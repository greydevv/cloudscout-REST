from flask import make_response, Response
from typing import List, Any

class ApiException(Exception):
    def __init__(self, **kwargs):
        self.response = {}
        if hasattr(self, 'message'):
            self.response['msg'] = self.message
        elif hasattr(self, 'msg'):
            self.response['msg'] = self.msg
        if kwargs:
            self.response = self.response | kwargs

    def get_response(self) -> Response:
        return make_response(self.response, self.code)

class AuthorizationError(ApiException):
    """
    Raised when authorization fails for a protected resource.
    """
    def __init__(self, code=401, msg='Unauthorized', **kwargs):
        super().__init__(code=code, msg=msg, **kwargs)
        self.code = code
        self.msg = msg

class DuplicateKeyError(ApiException):
    """
    Raised when an insertion POST request is made with an element that would
    create a duplicate key entry if it were to be entered into the database.
    """
    code = 409
    msg = 'Could not add element to database as doing so would cause duplicate entries'

class ResourceNotFoundError(ApiException):
    """
    Raised when a requested resource is not found in the database. This is
    usually determined by means of a primary key such as the 'pid' or 'uid'
    properties.
    """
    code = 404
    msg = 'Resource does not exist in the database'

class InvalidJsonError(ApiException):
    """
    Raised when the received JSON is invalid according to the defined schemas.
    """
    code = 400
    def __init__(self, msg, **kwargs):
        super().__init__(code=self.code, msg=msg, **kwargs)
        self.msg = msg
