from microservice.models.basesqlalchemy import Base, Helper
from sqlalchemy import (
        Table,
        Column,
        Index,
        ForeignKey,
        Boolean,
        Numeric,
        Integer,
        String,
        DateTime,
    )

class BlackTea(Base,Helper):
    __tablename__ = 'black'
    # __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}

    id=Column(Integer, primary_key=True)
    name=Column(String(100), nullable=False)
    origin=Column(String(100))

    def __init__(self,id=None,name=None):
        self.id = id
        self.name = name

    def to_dict(self,exclude=None):
        return super(BlackTea,self).to_dict(exclude)
