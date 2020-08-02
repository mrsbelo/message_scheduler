import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import force_auto_coercion

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///")

ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
force_auto_coercion()
BaseModel = declarative_base()

session = SessionLocal()
