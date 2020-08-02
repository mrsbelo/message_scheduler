import pytest

from app import app, db


def clean_database():
    db.drop_all()
    db.create_all()
    db.session.commit()


@pytest.fixture(name="prepare_db", scope="function")
def fixture_prepare_db():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    clean_database()

    return db


@pytest.fixture(name="save_instance", scope="function")
def fixture_save_instance():
    def _save_instance(model, data):
        data_to_db = model(**data)
        db.session.add(data_to_db)
        db.session.commit()

    return _save_instance


@pytest.fixture(name="flask_client", scope="function")
def fixture_flask_client():
    app.testing = True
    clean_database()

    return app.test_client()
