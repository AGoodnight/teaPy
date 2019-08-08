from pyramid.view import view_config
from pyramid.httpexceptions import (
        HTTPOk,
        HTTPNoContent,
        HTTPNotFound,
        HTTPConflict,
        HTTPBadRequest,
    )

from formencode import validators
#from pyramid_simpleform import Form

from microservice.handlers.base import BaseHandler, BaseSchema

from microservice.models.black import BlackTea

class TeaSchema(BaseSchema):
    tea_id = validators.Int(not_empty=False, if_missing=None)

class Handler(BaseHandler):

    @view_config(route_name="tea/black/{id}", renderer='json')
    def get_black_tea(self):
        print('GetBlackTea')
        form = self._validate_request(TeaSchema)
        response = self.get_tea(**form.data)
        return response

    def get_black_tea(self,tea_id=None):
        response = {}
        teaResult = self.db.query(BlackTea).filter_by(id=tea_id).one_or_none()
        if not teaResult:
            return HTTPNotFOund("No Tea Found")

    responseList = list(response.values())
    return responseList
