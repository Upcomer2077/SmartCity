# from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.models import *

engine = create_engine(
    "postgresql://postgres:pass@localhost:5432/postgres")
Base.metadata.create_all(bind=engine)

_Session = sessionmaker(bind=engine)

session = _Session()
