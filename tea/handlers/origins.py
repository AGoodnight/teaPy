from pyramid.response import Response
from pyramid.view import view_config
from tea.handlers.base import BaseHandler
from tea.models.origins import Origins

from colander import MappingSchema as Schema
from deform import Form, ValidationFailure


class Handler(BaseHandler):
    @view_config(route_name='origins', request_method='GET', renderer='json')
    def get_origins(self):
        return []
