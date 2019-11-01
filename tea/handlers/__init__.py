from pyramid.exceptions import Forbidden, NotFound
from tea.handlers.base import BaseHandler


def includeme(config):

    # core route changes
    config.add_view(BaseHandler.forbidden, context=Forbidden)
    config.add_view(BaseHandler.notfound, context=NotFound)

    config.add_route('hello', '/')
    config.add_route('tea', '/tea')
    config.add_route('flavors', '/flavors')
    config.add_route('origins', '/origins')
