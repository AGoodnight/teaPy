from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from session import Session
from models import *
from models import Origins

def create_list(model):
    session = Session().session
    list = []
    for instance in session.query(model):
        list.append({
            'id':instance.id,
            'name':instance.name,
            'origin':instance.origin.country,
            'flavors':instance.flavors
        })
    return list

@view_config(route_name='hello', request_method='GET')
def tea_time(request):
    return Response('Tea Time')

@view_config(route_name='all_tea', request_method='GET', renderer='json')
def get_all_tea(request):
    list = {}
    list['Black'] = create_list(BlackTea)
    list['Green'] = create_list(GreenTea)
    list['White'] = create_list(WhiteTea)
    list['Red'] = create_list(RedTea)
    list['Herbal'] = create_list(HerbalTea)
    return list

@view_config(route_name='black_tea', request_method='GET', renderer='json')
def get_black_tea(request):
    return create_list(BlackTea)

@view_config(route_name='green_tea', request_method='GET', renderer='json')
def get_green_tea(request):
    return create_list(GreenTea)

@view_config(route_name='white_tea', request_method='GET', renderer='json')
def get_white_tea(request):
    return create_list(WhiteTea)

@view_config(route_name='red_tea', request_method='GET', renderer='json')
def red_tea(request):
    return create_list(RedTea)

@view_config(route_name='herbal_tea', request_method='GET', renderer='json')
def get_herbal_tea(request):
    return create_list(HerbalTea)

@view_config(route_name='flavors', request_method='GET', renderer='json')
def get_black_flavors(request):
    session = Session().session
    list = []
    for instance in session.query(BlackTea.flavors).distinct():
        list.append(instance[0])

    uniques = []
    for value in list:
        items = value.split(',')
        for item in items:
            if item.strip() not in uniques:
                uniques.append(item.strip())

    return uniques


if __name__ == '__main__':

    with Configurator() as config:
        config.add_route('hello','/')
        config.add_route('all_tea','/tea')
        config.add_route('flavors','/flavors')
        config.add_route('black_tea','/tea/black')
        config.add_route('green_tea','/tea/green')
        config.add_route('red_tea','/tea/red')
        config.add_route('white_tea','/tea/white')
        config.add_route('herbal_tea','/tea/herbal')
        config.scan()
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0',6543,app)
    server.serve_forever()
