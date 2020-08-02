import pytest
from marshmallow import ValidationError

from app.schemas import UserSchema


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
