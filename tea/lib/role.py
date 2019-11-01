from pyramid.authentication import SessionAuthenticationPolicy
from tea.lib.helper import Util

import logging
log = logging.getLogger(__name__)


# this is used by pyramids core acl functionality
# given the logged in user pyramid identified in request
def get_roles(user_id, request):
    payload = Util.get_payload(request)
    roles = payload.get('roles', [])
    if user_id:
        # add a role that will be unique to this user only
        # used elsewhere to implement acl ownership functionality
        roles.append(user_id)

    return roles

# this is used as the Authentication Policy for Pyramid,
#  which retrieves the user id


class CustomAuthenticationPolicy(SessionAuthenticationPolicy):

    def authenticated_userid(self, request):
        payload = Util.get_payload(request)
        user_id = payload.get('user_id', None)
        return user_id

    def unauthenticated_userid(self, request):
        return self.authenticated_userid(request)
