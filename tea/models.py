from base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr, AbstractConcreteBase
from sqlalchemy.orm import relationship

class Origins(Base):
    __tablename__='origins'
    country=Column(String)

class Tea(AbstractConcreteBase, Base):

    name=Column(String)

    @declared_attr
    def origin_id(cls):
        return Column(ForeignKey('origins.id'))

    @declared_attr
    def origin(cls):
        return relationship('Origins')

class BlackTea(Tea):
    __tablename__ = 'black'
    flavors = Column(String)

class GreenTea(Tea):
    __tablename__ = 'green'

class WhiteTea(Tea):
    __tablename__ = 'white'

class RedTea(Tea):
    __tablename__ = 'red'

class HerbalTea(Tea):
    __tablename__ = 'herbal'
