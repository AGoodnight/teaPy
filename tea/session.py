from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Session:

    session = None
    engine = None

    def __init__(self):
        engine = create_engine('postgresql://postgres:root@localhost:5432/tea')
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

    def __repr__(self):
        return self
