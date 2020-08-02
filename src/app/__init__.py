from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from .decorators import error_handler
from .logs import get_logger
from .schemas import UserSchema

logger = get_logger(__name__)
app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
from .models import User


@app.route("/healthcheck", methods=["GET"])
def hello_world():
    logger.info("healthcheck")
    return jsonify({"status": "ok"})


@app.route("/users", methods=["GET", "POST"])
@error_handler
def users():
    if request.method == "GET":
        logger.info("users.request: %s", request)
        users_db = db.session.query(User).all()
        response = UserSchema().dump(users_db, many=True)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "POST":
        logger.info("users.request: %s", request)
        validated_request = UserSchema().load(request.json)
        logger.info("users.validated_request: %s", validated_request)

        user = User(**validated_request)
        db.session.add(user)
        db.session.commit()

        response = UserSchema().dump(user)
        logger.info("users.response: %s", response)

        return jsonify(response), HTTPStatus.CREATED.value
