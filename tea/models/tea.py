from tea.models.basesqlalchemy import Base, Helper
from tea.models.origins import Origins
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref


class Tea(Base, Helper):

    __tablename__ = 'kinds'

    name = Column(String)
    flavors = Column(String)

    origin_id = Column(Integer, ForeignKey('origins.id'))
    origin = relationship('Origins', backref=backref('kinds'))

    def to_dict(self):
        return super(Tea, self).to_dict()
