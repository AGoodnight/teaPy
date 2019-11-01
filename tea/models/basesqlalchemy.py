import datetime
from sqlalchemy.ext.declarative import (
        as_declarative,
        declared_attr,
        declarative_base
    )
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
    )
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import event
from sqlalchemy.pool import Pool
from sqlalchemy.exc import DisconnectionError


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Helper(object):

    def __init__(self, **kargs):
        columns = self.__class__.__table__.columns.keys()
        for column in columns:
            if column in kargs:
                val = kargs[column]
            else:
                val = Non
            setattr(self, column, val)

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
