class Success(object):
    SUCCESS_RESPONSE = "Successful"

    USER_CREATE_SUCCESS = "User added successfully."
    FILE_UPLOAD_SUCCESS = "File uploaded Successfully."
    FILE_DELETE_SUCCESS = "File deleted Successfully."
    FILE_FETCH_SUCCESS = "Files fetched Successfully."

    FILE_DELETE_SUCCESS_FROM_S3 = "File deleted successfully from S3."


class Error(object):
    ERROR_RESPONSE = "Error"
    SERVER_ERROR_5XX = "SERVER ERROR"
    EXCEPTION = "Some Unexpected Exception Occured. Error is "

    USER_CREATION_ERROR = "Error in adding User."
    FILE_UPLOAD_ERROR = "Error in uploading file."
    FILE_DELETE_ERROR = "Error in deleting file."
    FILE_FETCHING_ERROR = "Error in fetching files."
    FILE_COMPRESS_ERROR = "Error in compressing file."
    FILE_SIZE_COMPUTE_ERROR = "Error in computing file size."
    FILE_NOT_EXISTS_IN_DB = "This file_url does not exist in database for this user."

    INVALID_FILE_URL = "This is not a valid s3 url. Does not Exist."
    USER_ID_FETCH_ERROR = "Error in fetch user_id from token"
