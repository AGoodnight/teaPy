import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound

from formencode import Schema
from pyramid_simpleform import Form

from microservice.lib.helper import Util
from microservice.handlers.exception import InvalidRequestData
from microservice.models.basesqlalchemy import DBSession


class BaseHandler(object):

    def __init__(self, request):
        self.request = request
        self.db = DBSession()
        self.payload = Util.get_payload(request)
        self.rdata = self._load_data(request)
        self.req_id = request.headers.get('X-Request-Id','')
        request.add_response_callback(self.add_json_header)
        request.add_response_callback(self.add_cors_headers)

    @classmethod
    def forbidden(cls, request):
        return HTTPForbidden(body='{}')

    @classmethod
    def notfound(cls, request):
        return HTTPNotFound(body='{}')

    @classmethod
    def add_json_header(cls, request, response):
        response.content_type = 'application/json'
        return None

    @classmethod
    def add_cors_headers(cls, request, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = \
         'OPTIONS,GET,POST,PUT'
        response.headers['Access-Control-Allow-Headers'] = \
         'Accept,Content-Type,Authorization,Payload,Access-Control-Allow-Origin'
        response.headers['Access-Control-Expose-Headers'] = 'Authorization'
        return None

    def _load_data(self, request):
        data = {}
        data.update(request.GET)
        data.update(request.POST)
        try:
            data.update(request.json_body)
        except: pass
        data.update(request.matchdict)
        data['_cookies'] = request.cookies
        data['_method'] = request.method
        return FakeRequest(data)

    def _validate_request(self, Schema):
        method = self.rdata['_method']
        self.rdata['_method'] = 'POST'
        form = Form(self.rdata, schema=Schema)
        if not form.validate():
            raise InvalidRequestData(form.errors)
        self.rdata['_method'] = method
        return form

class FakeRequest(dict):
    @property
    def method(self):
        return self.get('_method', '')
    @property
    def GET(self):
        return self
    @property
    def POST(self):
        return self
    @property
    def params(self):
        return self
    @property
    def matchdict(self):
        return self
    @property
    def cookies(self):
        return self.get('_cookies', {})
    @property
    def localizer(self):
        return self
    @property
    def translate(self):
        return self

class BaseSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
