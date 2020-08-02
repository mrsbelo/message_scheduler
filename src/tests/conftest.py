import pytest

from app import app, session
from app.db import BaseModel, ENGINE


def clean_database():
    BaseModel.metadata.drop_all(bind=ENGINE)
    BaseModel.metadata.create_all(bind=ENGINE)
    session.commit()


@pytest.fixture(name="prepare_db", scope="function")
def fixture_prepare_db():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    clean_database()

    return session


@pytest.fixture(name="save_instance", scope="function")
def fixture_save_instance():
    def _save_instance(model, data):
        data_to_db = model(**data)
        session.add(data_to_db)
        session.flush()
        session.commit()

        return data_to_db

    return _save_instance


@pytest.fixture(name="flask_client", scope="function")
def fixture_flask_client():
    app.testing = True
    clean_database()

    return app.test_client()
