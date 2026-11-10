from database.db import SessionLocal
from database.models import Settings
from database.models import Meeting
from database.models import (
    Settings,
    Meeting,
    Note,
    Person
)

def save_settings(
    teams_url,
    file_format
):

    db = SessionLocal()

    settings = (
        db.query(Settings)
        .first()
    )

    if settings is None:

        settings = Settings()

        db.add(settings)

    settings.teams_url = teams_url
    settings.file_format = file_format

    db.commit()

    db.close()


def get_settings():

    db = SessionLocal()

    settings = db.query(Settings).first()

    db.close()

    return settings

def create_meeting(title):

    db = SessionLocal()

    meeting = Meeting(
        title=title
    )

    db.add(meeting)

    db.commit()

    db.refresh(meeting)

    db.close()

    return meeting

def get_meeting(
    meeting_id
):

    db = SessionLocal()

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    db.close()

    return meeting

def get_meetings():

    db = SessionLocal()

    meetings = (
        db.query(Meeting)
        .order_by(
            Meeting.id.desc()
        )
        .all()
    )

    db.close()

    return meetings


def save_note(
    meeting_id,
    timestamp,
    content
):

    db = SessionLocal()

    note = Note(
        meeting_id=meeting_id,
        timestamp=timestamp,
        content=content
    )

    db.add(note)

    db.commit()

    db.close()

def get_notes(
    meeting_id
):

    db = SessionLocal()

    notes = (
        db.query(Note)
        .filter(
            Note.meeting_id
            == meeting_id
        )
        .all()
    )

    db.close()

    return notes

def update_meeting_audio(
    meeting_id,
    audio_path
):

    db = SessionLocal()

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    if meeting:

        meeting.audio_path = (
            audio_path
        )

        db.commit()

    db.close()

def save_transcript(
    meeting_id,
    transcript
):

    db = SessionLocal()

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    if meeting:

        meeting.transcript = (
            transcript
        )

        db.commit()

    db.close()

def save_minutes(
    meeting_id,
    minutes
):

    db = SessionLocal()

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    if meeting:

        meeting.minutes = minutes

        db.commit()

    db.close()

def get_meeting(
    meeting_id
):

    db = SessionLocal()

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    db.close()

    return meeting

def add_person(name):

    print("DB登録:", name)

    db = SessionLocal()

    person = Person(
        name=name
    )

    db.add(person)

    db.commit()

    db.close()

    print("DB登録完了")

def get_persons():

    db = SessionLocal()

    persons = (
        db.query(Person)
        .all()
    )

    db.close()

    return persons

def delete_person_by_name(name):

    db = SessionLocal()

    person = (
        db.query(Person)
        .filter(
            Person.name == name
        )
        .first()
    )

    if person:

        db.delete(person)

        db.commit()

    db.close()