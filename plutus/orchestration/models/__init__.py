import os

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(os.environ.get("PLUTUS_DB_URI"))


class Base(DeclarativeBase):
    pass


ACTIVE_STATUS_ENUM = ENUM("ACTIVE", "INACTIVE", name="active_status_enum")
