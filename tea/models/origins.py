from tea.models.basesqlalchemy import Base, Helper
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr, AbstractConcreteBase
from sqlalchemy.orm import relationship


class Origins(Base, Helper):
    __tablename__ = 'origins'
    country = Column(String)
