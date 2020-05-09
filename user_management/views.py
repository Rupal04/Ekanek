import logging

from rest_framework.decorators import api_view, permission_classes
from user_management.utility import add_user, upload, delete, fetch_user_files, fetch_user_id_from_token
from user_management.response import ErrorResponse,ServerErrorResponse
from user_management.constant import Error
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_user(request):
    try:
        data = request.data
        response = add_user(data)

        if not response:
            response = ErrorResponse(msg=Error.USER_CREATION_ERROR)
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response and response.success is False:
            return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.__dict__, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(Error.EXCEPTION + str(e))
        response = ServerErrorResponse()
        return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    try:
        data=request.data

        user_id = fetch_user_id_from_token(request.auth)
        file_path = data.get('file_path', None)
        file_name = data.get('file_name', None)
        description = data.get('description', None)

        response = upload(user_id,file_path,file_name,description)

        if not response:
            response = ErrorResponse(msg=Error.FILE_UPLOAD_ERROR)
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response and response.success is False:
            return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.__dict__, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(Error.EXCEPTION + str(e))
        response = ServerErrorResponse()
        return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_file(request):
    try:
        data = request.data

        file_url = data.get("file_url",None)
        user_id = fetch_user_id_from_token(request.auth)

        response = delete(file_url, user_id)

        if not response:
            response = ErrorResponse(msg=Error.FILE_DELETE_ERROR)
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response and response.success is False:
            return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.__dict__, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(Error.EXCEPTION + str(e))
        response = ServerErrorResponse()
        return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_files(request):
    try:

        user_id = fetch_user_id_from_token(request.auth)

        if user_id:
            response = fetch_user_files(user_id)

            if not response:
                response = ErrorResponse(msg=Error.FILE_FETCHING_ERROR)
                return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

            return Response(response.__dict__, status=status.HTTP_200_OK)
        else:
            response = ErrorResponse(msg=Error.USER_ID_FETCH_ERROR)
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(Error.EXCEPTION + str(e))
        response = ServerErrorResponse()
        return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
