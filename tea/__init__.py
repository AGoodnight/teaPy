from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='hello', request_method='GET')
def tea_time(request):
    return Response('Tea Time')


def main(global_config, **settings):
    with Configurator() as config:
        config.scan('tea.models')
        config.include('tea.handlers')
        config.scan('tea.handlers')

    return config.make_wsgi_app()
