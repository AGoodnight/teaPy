import os
import re
import string
import random
import hashlib
import json

from pyramid.security import authenticated_userid

import logging
log = logging.getLogger(__name__)


class Util(object):

    @classmethod
    def get_payload(cls, request):
        payload_header = request.headers.get('Payload')
        try:
            payload = json.loads(payload_header)
        except Exception:
            payload = {}
        return payload

    @classmethod
    def make_payload(cls, user):
        roles = [role.name for role in user.roles]
        payload = {'user_id': user.id, 'roles': roles}
        return payload

    @classmethod
    def has_roles(cls, roles, payload):
        return bool(set(roles).intersection(payload['roles']))

    @classmethod
    def hash_pass(cls, password, salt='', request=None):
        if request:
            salt = request.registry.settings['microservice.password.salt']
        digest = hashlib.sha256()
        digest.update(password.encode('utf-8'))
        digest.update(salt.encode('utf-8'))
        return digest.hexdigest()

    @classmethod
    def make_random_string(cls, length=16):
        return ''.join(random.choice(string.ascii_letters + string.digits)
                       for i in range(length))

# shim for PasteDeploy
# paste/deploy/loadwsgi.py
# need following line of code added after line 390:
#  defaults.update(os.environ)


class INIHelper(object):

    # make a regex that matches on ${ENV} throughout a string,
    # for all current environment varables
    ENV_VARS = dict(os.environ)
    MATCH_ENV_VARS = \
     re.compile(r'\$\{\b(' + '|'.join(ENV_VARS.keys()) + r')\b\}')

    # loop through each value and replace all ${ENV} occurances with
    # that environment variable's actual value
    @classmethod
    def replace_env_vars(cls, settings):
        for key in settings:
            settings[key] = cls.MATCH_ENV_VARS.sub(cls._get_env_var_value,
                                                   settings[key])
        return cls

    # given a env var name matched in the string, get it's value
    @classmethod
    def _get_env_var_value(cls, match_object):
        matched_text = match_object.group(1)
        env_var_value = cls.ENV_VARS[matched_text]
        return env_var_value
