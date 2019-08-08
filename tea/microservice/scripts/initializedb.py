import argparse
import transaction

from pyramid.paster import (
        get_appsettings,
        setup_logging,
    )

from sqlalchemy import engine_from_config
from microservice.models.basesqlalchemy import DBSession, Base
from microservice.models.black import BlackTea

#from microservice.lib.helper import Util, INISecretsManager as INIHelper
from microservice.lib.helper import Util, INIHelper

def main():
    # get command line args
    args = argparse.ArgumentParser()
    args.add_argument('config', type=str)
    args.add_argument('--clear', action='store_true', help='Enabling this option clears out the DB')
    args = args.parse_args()

    setup_logging(args.config)
    settings = get_appsettings(args.config)
    INIHelper(settings).replace_env_vars()

    # get user db connection
    engine = engine_from_config(settings, 'sqlalchemy.microservice.')
    DBSession.configure(bind=engine)

    # If specified, clear out the database
    if args.clear:
        Base.metadata.drop_all(engine)

    # create the db tables
    Base.metadata.create_all(engine)

    # insert db data
    with transaction.manager:
        load_core_data(args)

    return None

def load_core_data(args):

    return None

# initialize database
if __name__ == '__main__':
    main()
