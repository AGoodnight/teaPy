import logging
log = logging.getLogger(__name__)


# add app name to json logger
from pythonjsonlogger import jsonlogger
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        ret = super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['app'] = 'auth'
        return ret

# Log wrapper to add logging to each decorator
import time
from functools import wraps
def log_wrapper(wrapped):
    @wraps(wrapped)
    def wrapper(self):
        start = time.time()
        response = wrapped(self)
        duration = time.time() - start
        #response.headers['X-View-Time'] = '%.3f' % (duration,)
        log.info(self.request, 
                 extra={
                     "resp_time": duration, 
                     "user_id": self.user_id, 
                     "headers": dict(self.request.headers), 
                     "request_id": self.req_id
                 })
        return response
    return wrapper

