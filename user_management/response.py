from user_management.constant import Success, Error


class SuccessResponse(object):
    def __init__(self, results=None, msg=Success.SUCCESS_RESPONSE):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True


class ErrorResponse(object):
    def __init__(self, msg=Error.ERROR_RESPONSE):
        self.msg = msg
        self.success = False


class ServerErrorResponse(object):
    def __init__(self, msg=Error.SERVER_ERROR_5XX):
        self.msg = msg
        self.success = False
