import logging
import boto3
import os
import gzip
import shutil
from http import client
from urllib.parse import urlparse


from ekanek.conf import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    S3_BUCKET,
    S3_LOCATION,
    DESTINATION_FILE_BASE_PATH,
    UPLOAD_DIR
    )
from user_management.response import SuccessResponse, ErrorResponse
from user_management.constant import Success, Error
from user_management.serializers import UserSerializer, FileSystemSerializer
from user_management.models import FileSystem
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)


def add_user(data):
    try:
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)

        if user_obj:
            user_obj.set_password(password)
            user_obj.save()

            serialized_user_obj = UserSerializer(user_obj)
            return SuccessResponse(msg=Success.USER_CREATE_SUCCESS, results=serialized_user_obj.data)
        else:
            return ErrorResponse(msg=Error.USER_CREATION_ERROR)

    except Exception as e:
        logger.error(Error.USER_CREATION_ERROR + str(e))
        return None


# create an connection for S3 AWS service
s3_conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)


def upload_to_s3(file, file_name, upload_dir=UPLOAD_DIR, acl='public-read'):
    try:
        s3_conn.upload_fileobj(
            file,
            S3_BUCKET,
            "/".join([upload_dir, file_name]),
            ExtraArgs={'ACL': acl}
        )

        s3_location = S3_LOCATION.format(S3_BUCKET)

        destination_file_url = "/".join([s3_location, upload_dir,
                                         file_name])

        return destination_file_url

    except Exception as e:
        raise Exception(Error.FILE_UPLOAD_ERROR + str(e))


def url_exists(file_url):
    _, host, path, _, _, _ = urlparse(file_url)
    conn = client.HTTPConnection(host)
    conn.request('HEAD', path)
    return conn.getresponse().status < 400


def delete_from_s3(file_url=""):
    try:
        is_valid = url_exists(file_url)

        if is_valid:
            bucket_file_prefix = S3_LOCATION.format(S3_BUCKET)

            # check if file_url starts with bucket file prefix
            if not file_url.startswith(bucket_file_prefix):
                raise Exception("%s not starts with %s" % (file_url,
                                                           bucket_file_prefix))

            # remove bucket file prefix from file_url to get key name of file
            file_key_name = file_url[len(bucket_file_prefix) + 1:]

            s3_conn.delete_object(
                Bucket=S3_BUCKET,
                Key=file_key_name
            )

            return True
        else:
            logger.error(Error.INVALID_FILE_URL)
            return False

    except Exception as e:
        raise Exception(Error.FILE_DELETE_ERROR + str(e))


def create_compressed_file(file_path, file_name):
    try:
        compressed_filename = os.path.splitext(file_name)[0] + ".gz"
        destination_filepath = DESTINATION_FILE_BASE_PATH + compressed_filename

        with open(file_path, 'rb') as f_in:
            with gzip.open(destination_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(destination_filepath, 'rb') as c_file:
            return upload_to_s3(c_file, compressed_filename)

    except Exception as e:
        raise Exception(Error.FILE_COMPRESS_ERROR + str(e))


def get_file_size_in_gb(file_path):
    try:
        size_in_bytes = os.path.getsize(file_path)
        size_in_gb = size_in_bytes / (1024 * 1024 * 1024)
        return size_in_gb
    except Exception as e:
        raise Exception(Error.FILE_SIZE_COMPUTE_ERROR + str(e))


def upload(user_id, file_path, file_name, description):
    try:
        file_type = None
        s3_url = None

        file_type = os.path.splitext(file_name)[1]
        file_size_in_gb = get_file_size_in_gb(file_path)

        if file_size_in_gb > 1:
            s3_url = create_compressed_file(file_path, file_name)
        else:
            with open(file_path, 'rb') as file:
                s3_url = upload_to_s3(file, file_name)

        file_obj = FileSystem.objects.create(user_id=user_id, s3_file_url=s3_url,
                                             title=file_name, file_type=file_type,
                                             file_size_in_gb=file_size_in_gb)
        if description:
            file_obj.description = description
            file_obj.save()

        serialized_file_obj = FileSystemSerializer(file_obj)
        return SuccessResponse(msg=Success.FILE_UPLOAD_SUCCESS, results=serialized_file_obj.data)

    except Exception as e:
        logger.error(Error.FILE_UPLOAD_ERROR + str(e))
        return None


def delete(file_url,user_id):
    try:
        if FileSystem.objects.filter(s3_file_url=file_url, user_id=user_id).exists():
            FileSystem.objects.filter(s3_file_url=file_url, user_id=user_id).delete()

            is_deleted = delete_from_s3(file_url)

            if is_deleted:
                logger.info(Success.FILE_DELETE_SUCCESS_FROM_S3)
            else:
                logger.info(Error.INVALID_FILE_URL)

            return SuccessResponse(msg=Success.FILE_DELETE_SUCCESS)
        else:
            return ErrorResponse(msg=Error.FILE_NOT_EXISTS_IN_DB)

    except Exception as e:
        logger.error(Error.FILE_DELETE_ERROR + str(e))
        return None


def fetch_user_files(user_id):
    try:
        if FileSystem.objects.filter(user=user_id).exists():
            files = FileSystem.objects.filter(user=user_id)

            result = []
            for file in files:
                serialized_file_obj = FileSystemSerializer(file)
                result.append(serialized_file_obj.data)

            return SuccessResponse(msg=Success.FILE_FETCH_SUCCESS, results=result)
        else:
            return ErrorResponse(msg=Error.FILE_FETCHING_ERROR)

    except Exception as e:
        logger.error(Error.FILE_FETCHING_ERROR + str(e))
        return None


def fetch_user_id_from_token(token):
    try:
        token = Token.objects.get(key=token)
        return token.user_id
    except Exception as e:
        logger.error(Error.USER_ID_FETCH_ERROR + str(e))
        return None
