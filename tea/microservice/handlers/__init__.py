from pyramid.exceptions import Forbidden, NotFound
from microservice.handlers.base import BaseHandler

def includeme(config):

    print("hello")

    # core route changes
    config.add_view(BaseHandler.forbidden, context=Forbidden)
    config.add_view(BaseHandler.notfound, context=NotFound)

    # cors
    # doesn't actually need handler, all responses get cors added
    config.add_route('CORS', '/{cors:.*}', request_method='OPTIONS')

    # system tests
    config.add_route('TestCORS', '/test/cors')
    config.add_route('Ping', '/ping')
    config.add_route('PingDB', '/ping/db')

    # Vehicle data
    config.add_route('GetBlackTea', '/tea/black/{id}', request_method='GET')
