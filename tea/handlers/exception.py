import logging
log = logging.getLogger(__name__)

import json
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound


class BadRequest(HTTPBadRequest):
    def __init__(self, error=None):
        if hasattr(self, 'STATUS_CODE'):
            self.code = self.STATUS_CODE
        err = {'type': self.TYPE}
        if error:
            err['error'] = error
        super(BadRequest, self).__init__(body=json.dumps(err))

class NotImplemented(BadRequest):
    TYPE = 'not_implemented'

# throw this instead of a 500
class DataError(BadRequest):
    TYPE = 'data_error'

# for bad input fields
class InvalidRequestData(BadRequest):
    TYPE = 'invalid_request_data'

# for login
class AccountInactive(BadRequest):
    TYPE = 'account_inactive'
    STATUS_CODE = 401
class InvalidLogin(BadRequest):
    TYPE = 'login_failed'
    STATUS_CODE = 401

# for password reset
class InvalidCode(BadRequest):
    TYPE = 'invalid_code'
