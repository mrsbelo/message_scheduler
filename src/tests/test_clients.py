from datetime import datetime, timedelta

import pytest

from app.clients import check_if_message_exists, is_user_ok_to_recieve_this_kind
from app.constants import KIND_MAP
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


@pytest.mark.parametrize(
    "kind, expected_result",
    [("email", False), ("sms", True), ("push", False), ("whatsapp", True)],
)
def test_is_user_ok_to_recieve_this_kind_user_missing_email(
    prepare_db, save_instance, kind, expected_result
):
    _ = prepare_db
    user_db = save_instance(User, {"name": "marco", "phone": "1234567"})
    data = {"kind": KIND_MAP[kind], "user_id": user_db.id}

    assert is_user_ok_to_recieve_this_kind(data) == expected_result


@pytest.mark.parametrize(
    "kind, expected_result",
    [("email", True), ("sms", False), ("push", True), ("whatsapp", False)],
)
def test_is_user_ok_to_recieve_this_kind_user_missing_phone(
    prepare_db, save_instance, kind, expected_result
):
    _ = prepare_db
    user_db = save_instance(User, {"name": "marco", "email": "asd@asd.com",})
    data = {"kind": KIND_MAP[kind], "user_id": user_db.id}

    assert is_user_ok_to_recieve_this_kind(data) == expected_result
