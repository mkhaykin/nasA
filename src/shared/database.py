import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
SessionLocal = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)
