from datetime import timedelta

from .constants import KIND_MAP
from .db import session
from .models import Message, User


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


def get_user_by_id(user_id):
    return session.query(User).get(user_id)


def is_user_ok_to_recieve_this_kind(user_db, data):
    if data["kind"] in [KIND_MAP["email"], KIND_MAP["push"]]:
        if not user_db.email:
            return False
    elif data["kind"] in [KIND_MAP["sms"], KIND_MAP["whatsapp"]]:
        if not user_db.phone:
            return False

    return True
