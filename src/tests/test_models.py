from hamcrest import assert_that, has_entries
from sqlalchemy.exc import IntegrityError

from app.models import User


def test_user_create(prepare_db):
    db = prepare_db
    data = {"name": "marco", "email": "asd@asd.com", "phone": "1234567"}
    user = User(**data)
    data["id"] = 1
    db.session.add(user)
    db.session.commit()
    user.id
    assert_that(user.__dict__, has_entries(data))
    db.session.rollback()


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
        db.session.rollback()


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
        db.session.rollback()


def test_user_empty_data(prepare_db, save_instance):
    db = prepare_db
    try:
        save_instance(User, {})
    except IntegrityError as exc:
        assert exc.args == (
            "(sqlite3.IntegrityError) NOT NULL constraint failed: user.name",
        )
        db.session.rollback()
