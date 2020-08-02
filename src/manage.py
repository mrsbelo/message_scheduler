from flask.cli import FlaskGroup
from app import app, session
from app.models import BaseModel
from app.db import ENGINE

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    BaseModel.metadata.drop_all(bind=ENGINE)
    BaseModel.metadata.create_all(bind=ENGINE)
    session.commit()


if __name__ == "__main__":
    cli()
