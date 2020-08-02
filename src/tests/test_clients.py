from datetime import datetime, timedelta

import pytest

from app.clients import check_if_message_exists
from app.models import Message, User


def test_check_if_message_exists_same_datetime(prepare_db, save_instance):
    utc_now = datetime.utcnow().replace(microsecond=0)
    _ = prepare_db
    user = save_instance(
        User, {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    )
    data = {
        "scheduled": utc_now,
        "text": "wake up",
        "kind": 1,
        "status": 1,
        "user_id": user.id,
    }
    _ = save_instance(Message, data)
    assert check_if_message_exists(data)


@pytest.mark.parametrize("minutes, exists", [(29, True), (30, False)])
def test_check_if_message_exists_29_minutes_down_and_30_minutes_down(
    prepare_db, save_instance, minutes, exists
):
    utc_now = datetime.utcnow().replace(microsecond=0)
    gap = utc_now - timedelta(minutes=minutes)
    _ = prepare_db
    user = save_instance(
        User, {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    )
    data = {
        "scheduled": utc_now,
        "text": "wake up",
        "kind": 1,
        "status": 1,
        "user_id": user.id,
    }
    _ = save_instance(Message, data)
    data["scheduled"] = gap
    result = True if check_if_message_exists(data) else False

    assert result == exists


@pytest.mark.parametrize("minutes, exists", [(29, True), (30, False)])
def test_check_if_message_exists_29_minutes_up_and_30_minutes_up(
    prepare_db, save_instance, minutes, exists
):
    utc_now = datetime.utcnow().replace(microsecond=0)
    gap = utc_now + timedelta(minutes=minutes)
    _ = prepare_db
    user = save_instance(
        User, {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    )
    data = {
        "scheduled": utc_now,
        "text": "wake up",
        "kind": 1,
        "status": 1,
        "user_id": user.id,
    }
    _ = save_instance(Message, data)
    data["scheduled"] = gap
    result = True if check_if_message_exists(data) else False

    assert result == exists
