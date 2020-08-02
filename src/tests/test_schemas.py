from datetime import datetime, timedelta

import pytest
from marshmallow import ValidationError

from app.constants import STATUS_MAP
from app.schemas import MessageSchema, UserSchema


def test_user_empty_data():
    try:
        UserSchema().load({})
    except ValidationError as exc:
        assert exc.messages == {"name": ["Missing data for required field."]}


def test_user_valid_data():
    data = {"name": "marco", "email": "asd@asd.com", "phone": "123456789"}
    result = UserSchema().load(data)

    assert result == data


@pytest.mark.parametrize(
    "email", ["a@", "aa.aa.aa", "@a", "aa@aa", "@aa.aa", "aa@aa@aa.aa"]
)
def test_user_email_validation(email):
    data = {"name": "marco", "email": email}

    try:
        UserSchema().load(data)
    except ValidationError as exc:
        assert exc.messages == {"email": ["Not a valid email address."]}


def test_message_empty_data():
    try:
        MessageSchema().load({})
    except ValidationError as exc:
        assert exc.messages == {
            "kind": ["Missing data for required field."],
            "scheduled": ["Missing data for required field."],
            "text": ["Missing data for required field."],
            "user_id": ["Missing data for required field."],
        }


def test_message_load_auto_fill_created_with_utc_and_microsecond_zero():
    data = {
        "scheduled": "2040-08-2T16:12:12Z",
        "text": "oijwqoid",
        "kind": "email",
        "status": "sended",
        "user_id": 1,
    }
    result = MessageSchema().load(data)
    expected_result = {
        "created": datetime.utcnow().replace(microsecond=0),
        "kind": 1,
        "scheduled": datetime(2040, 8, 2, 16, 12, 12),
        "status": 2,
        "text": "oijwqoid",
        "user_id": 1,
    }

    assert result == expected_result


def test_message_auto_fill_status_field():
    data = {
        "scheduled": "2030-08-2T16:12:12Z",
        "text": "oijwqoid",
        "kind": "email",
        "user_id": 1,
    }
    result = MessageSchema().load(data)
    assert result["status"] == STATUS_MAP["scheduled"]


@pytest.mark.parametrize(
    "status_input, status_output", [("scheduled", 1), ("sended", 2)]
)
def test_message_status_mapping_str_to_int_on_load(status_input, status_output):
    data = {
        "scheduled": "2040-08-2T16:12:12Z",
        "text": "oijwqoid",
        "kind": "email",
        "status": status_input,
        "user_id": 1,
    }
    result = MessageSchema().load(data)

    assert result["status"] == status_output


@pytest.mark.parametrize(
    "status_input, status_output", [(1, "scheduled"), (2, "sended")]
)
def test_message_status_mapping_int_to_str_on_dump(status_input, status_output):
    data = {
        "scheduled": datetime(2040, 8, 2, 16, 12, 12),
        "text": "oijwqoid",
        "kind": 1,
        "status": status_input,
        "user_id": 1,
    }
    result = MessageSchema().dump(data)

    assert result["status"] == status_output


@pytest.mark.parametrize(
    "kind_input, kind_output", [("email", 1), ("sms", 2), ("push", 3), ("whatsapp", 4)],
)
def test_message_kind_mapping_str_to_int_on_load(kind_input, kind_output):
    data = {
        "scheduled": "2040-08-2T16:12:12Z",
        "text": "oijwqoid",
        "kind": kind_input,
        "user_id": 1,
    }
    result = MessageSchema().load(data)

    assert result["kind"] == kind_output


@pytest.mark.parametrize(
    "kind_input, kind_output", [(1, "email"), (2, "sms"), (3, "push"), (4, "whatsapp")],
)
def test_message_kind_mapping_int_to_str_on_dump(kind_input, kind_output):
    data = {
        "scheduled": datetime(2040, 8, 2, 16, 12, 12),
        "text": "oijwqoid",
        "kind": kind_input,
        "status": 1,
        "user_id": 1,
    }
    result = MessageSchema().dump(data)

    assert result["kind"] == kind_output


def test_message_options_fields_invalid_options():
    data = {
        "scheduled": "2040-08-2T16:12:12Z",
        "text": "oijwqoid",
        "kind": "xxxx",
        "status": "xxxx",
        "user_id": 1,
    }
    try:
        MessageSchema().load(data)
    except ValidationError as exc:
        assert exc.messages == {
            "kind": ["Must be one of: email, sms, push, whatsapp."],
            "status": ["Must be one of: scheduled, sended."],
        }


@pytest.mark.parametrize("minutes_offset", [10, 0])
def test_message_schedule_cannot_be_older_than_utcnow_or_equal_to_utcnow(
    minutes_offset,
):
    _scheduled = datetime.utcnow().replace(microsecond=0) - timedelta(
        minutes=minutes_offset
    )
    scheduled = _scheduled.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "scheduled": scheduled,
        "text": "oijwqoid",
        "kind": "sms",
        "user_id": 1,
    }
    try:
        MessageSchema().load(data)
    except ValidationError as exc:
        assert exc.messages == {
            "scheduled": ["Cannot scheduled messages into the past"],
        }
