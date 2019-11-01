from pyramid.security import authenticated_userid
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from tea.session import Session
from tea.models.origins import Origins

from colander import MappingSchema, SchemaNode, Bool
from deform import Form, ValidationFailure

from tea.lib.helper import Util
from tea.handlers.exception import InvalidRequestData


class BaseHandler(object):

    def __init__(self, request):
        self.request = request
        self.db = Session().session
        self.payload = Util.get_payload(request)
        self.user_id = authenticated_userid(request)
        self.rdata = self._load_data(request)
        self.req_id = request.headers.get('X-Request-Id', '')
        request.add_response_callback(self.add_json_header)

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
            'Accept,Content-Type,Authorization,Payload'
        response.headers['Access-Control-Expose-Headers'] = 'Authorization'
        return None

    def _load_data(self, request):
        data = {}
        data.update(request.GET)
        data.update(request.POST)
        try:
            data.update(request.json_body)
        except Exception:
            pass
        data.update(request.matchdict)
        data['_cookies'] = request.cookies
        data['_method'] = request.method
        return FakeRequest(data)

    def _validate_request(self, Schema):
        method = self.rdata['_method']
        self.rdata['_method'] = 'POST'
        form = Form(Schema())
        try:
            print('Validating')
            print(self.rdata.items())
            validated = form.validate(self.rdata.items())
            print('Validation Finished')
        except ValidationFailure as e:
            raise e
        except Exception as e:
            raise InvalidRequestData(e)
        self.rdata['_method'] = method
        return validated

    def bind_form(self, obj, form, exclude=[]):
        for key in form:
            if hasattr(obj, key) and not key in exclude:
                setattr(obj, key, form[key])
        return obj


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


class BaseSchema(MappingSchema):
    filter_extra_fields = SchemaNode(Bool())
    allow_extra_fields = SchemaNode(Bool())
