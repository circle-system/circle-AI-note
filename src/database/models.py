from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)

    teams_url = Column(String)
    sharepoint_url = Column(String)
    document_format = Column(String)




class Meeting (Base):

    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    transcript = Column(Text)

    minutes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.now
    )