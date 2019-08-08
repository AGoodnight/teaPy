import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
    )
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import event
from sqlalchemy.pool import Pool
from sqlalchemy.exc import DisconnectionError


# this is our sqlalchemy database connection
# it can be accessed globally by importing from this module
# the concept is this keeps everything thread safe,
#   and allows database <-> object sequenciation to stay in line throughout
#   a single request
# this within a request concept is referred to as the database session
# Zope is a objct that ties sqlalchemy's session concept in with actual
#   database transactions
# the final piece is python's transaction package
#   and transaction.manager module
#       these are used to run all database modifications within transactions
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

# this is the class our sqlalchemy models will inherit from
Base = declarative_base()

# mysql will close idle connections after a while
# the following allows sqlalchemy to recover from this error,
# by checking its connection and making a new connection when needed,
# before attempting to run the query
@event.listens_for(Pool, 'checkout')
def mysql_pool_notimeout(dbapi_conn, connection_rec, connection_proxy):
    try:
        dbapi_conn.ping()
    except:
        raise DisconnectionError()

class Helper(object):

    # initialize all columns so that to_dict() returns them
    # even if they aren't specifically set
    def __init__(self, **kargs):
        columns = self.__class__.__table__.columns.keys()
        for column in columns:
            if column in kargs:
                val = kargs[column]
            else:
                val = None
            setattr(self, column, val)

    def set_from_dict(self, dict_):
        for key in dict_:
            if hasattr(self, key):
                setattr(self, key, dict_[key])
        return self

    def to_dict(self, exclude={}, encode_utf8=False):
        to_dict = {}
        for var in vars(self):
            if not var.startswith('_') and var not in exclude:
                val = getattr(self, var)
                if isinstance(val, datetime.datetime):
                    to_dict[var] = val.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(val, datetime.date):
                    to_dict[var] = val.strftime('%Y-%m-%d')
                elif isinstance(val, str) and encode_utf8:
                    to_dict[var] = val.encode('utf8', 'ignore')
                else:
                    to_dict[var] = val
        return to_dict

    def set_modified(self):
        self.modified = datetime.datetime.utcnow()
        return self
