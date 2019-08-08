from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# sqlalchemy
from sqlalchemy import engine_from_config
from microservice.models.basesqlalchemy import DBSession

@view_config(route_name='home', request_method='GET')
def first_tea(request):
    return Response('<h1>Have a Spot of Tea?</h2>')

def main(global_config, **settings):

    print("Hello")

    INIHelper(settings).replace_env_vars()

    engine = engine_from_config(settings,'sqlalchemy.microservice.')
    DBSession.configure(bind=engine)

    with Configurator() as config:
        config.add_route('home','/')
        config.scan('microservice.models')
        config.include('microservice.handlers')
        config.scan('microservice.handlers')
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0',6543,app)
    server.serve_forever()
