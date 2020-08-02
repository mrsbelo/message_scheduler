from datetime import timedelta

from .db import session
from .models import Message


def check_if_message_exists(data):
    gap_30_minutes_up = data["scheduled"] + timedelta(minutes=30)
    gap_30_minutes_down = data["scheduled"] - timedelta(minutes=30)
    return (
        session.query(Message)
        .filter_by(text=data["text"], kind=data["kind"], user_id=data["user_id"],)
        .filter(
            Message.scheduled < gap_30_minutes_up,
            Message.scheduled > gap_30_minutes_down,
        )
        .all()
    )
