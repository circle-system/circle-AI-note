from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Settings(Base):

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)

    teams_url = Column(String)

    sharepoint_url = Column(String)

    file_format = Column(String)




class Meeting(Base):

    __tablename__ = "meetings"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(String)

    transcript = Column(Text)

    minutes = Column(Text)

    audio_path = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.now
    )

class Note(Base):

    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id")
    )

    timestamp = Column(String)

    content = Column(Text)

class Person(Base):

    __tablename__ = "persons"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )