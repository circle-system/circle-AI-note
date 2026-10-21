from database.db import SessionLocal
from database.models import Settings
from database.models import Meeting


def save_settings(
    teams_url,
    sharepoint_url,
    document_format
):

    db = SessionLocal()

    setting = db.query(Settings).first()

    if setting is None:
        setting = Settings()

    setting.teams_url = teams_url
    setting.sharepoint_url = sharepoint_url
    setting.document_format = document_format

    db.add(setting)

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