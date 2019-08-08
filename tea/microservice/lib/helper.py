import logging
log = logging.getLogger(__name__)

import os
import re
import hashlib
import json

class Util(object):

    @classmethod
    def get_payload(cls, request):
        payload_header = request.headers.get('Payload')
        try:
            payload = json.loads(payload_header)
        except:
            payload = {}
        return payload


# shim for PasteDeploy
# paste/deploy/loadwsgi.py
# need following line of code added after line 390:
#  defaults.update(os.environ)
class INIHelper(object):

    def __init__(self, settings):
        self.settings = settings
        # make a regex that matches on ${ENV} throughout a string,
        #  for all current environment varables
        self.ENV_VARS = self._get_env_vars()
        self.MATCH_ENV_VARS = \
         re.compile(r'\$\{\b(' + '|'.join(self.ENV_VARS.keys()) + r')\b\}')

    # this can be redefined in subclass to get data from a different source
    def _get_env_vars(self):
        return dict(os.environ)

    # loop through each value and replace all ${ENV} occurances with
    #  that environment variable's actual value
    def replace_env_vars(self):
        for key in self.settings:
            self.settings[key] = self.MATCH_ENV_VARS.sub(
                                  self._get_env_var_value,
                                  self.settings[key])
        return self

    # given a env var name matched in the string, get it's value
    def _get_env_var_value(self, match_object):
        matched_text = match_object.group(1)
        env_var_value = self.ENV_VARS[matched_text]
        return env_var_value

class INISecretsManager(INIHelper):

    SECRET_NAME_ENV_VAR_SETTING = 'microservice.configs.secret_name.env_var'

    def _get_env_vars(self):
        sm = boto3.client('secretsmanager')

        # get the env var name we should look for,
        #  then get the secret name from it
        env_var_name = self.settings[self.SECRET_NAME_ENV_VAR_SETTING]
        secret_name = os.environ[env_var_name]

        # return the secrets stored as key/value pairs as a dict
        res = sm.get_secret_value(SecretId=secret_name)
        return json.loads(res['SecretString'])
