from datetime import datetime, timedelta

from hamcrest import assert_that, has_entries
from sqlalchemy.exc import IntegrityError

from app.models import Message, User


def test_user_create(prepare_db, save_instance):
    db = prepare_db
    data = {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    user = save_instance(User, data)
    data["id"] = 1
    _ = user.id
    assert_that(user.__dict__, has_entries(data))
    db.rollback()


def test_user_unique_email(prepare_db, save_instance):
    data = {"name": "marco", "email": "a@a.a"}
    db = prepare_db
    save_instance(User, data)
    try:
        save_instance(User, data)
    except IntegrityError as exc:
        assert exc.args == (
            "(sqlite3.IntegrityError) UNIQUE constraint failed: user.email",
        )
        db.rollback()


def test_user_unique_phone(prepare_db, save_instance):
    data = {"name": "marco", "phone": "12345"}
    db = prepare_db
    save_instance(User, data)
    try:
        save_instance(User, data)
    except IntegrityError as exc:
        assert exc.args == (
            "(sqlite3.IntegrityError) UNIQUE constraint failed: user.phone",
        )
        db.rollback()


def test_user_empty_data(prepare_db, save_instance):
    db = prepare_db
    try:
        save_instance(User, {})
    except IntegrityError as exc:
        assert exc.args == (
            "(sqlite3.IntegrityError) NOT NULL constraint failed: user.name",
        )
        db.rollback()


def test_message_create(prepare_db, save_instance):
    db = prepare_db
    user = save_instance(
        User, {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    )
    data = {
        "scheduled": datetime.utcnow().replace(microsecond=0) + timedelta(days=2),
        "text": "wake up",
        "kind": 1,
        "status": 0,
        "user_id": 1,
    }
    message = save_instance(Message, data)
    _ = message.id
    assert_that(message.__dict__, has_entries(data))
    db.rollback()


def test_delete_a_user_message_should_delete_on_cascade(prepare_db, save_instance):
    db = prepare_db
    user = save_instance(
        User, {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    )
    data = {
        "scheduled": datetime.utcnow().replace(microsecond=0) + timedelta(days=2),
        "text": "wake up",
        "kind": 1,
        "status": 0,
        "user_id": user.id,
    }
    message = save_instance(Message, data)
    db.delete(user)
    db.commit()
    result = db.query(Message).all()

    assert len(result) == 0
    db.rollback()
