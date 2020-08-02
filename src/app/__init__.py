from http import HTTPStatus

from flask import Flask, jsonify, request

from .db import session
from .decorators import error_handler
from .logs import get_logger
from .models import BaseModel, Message, User
from .schemas import UserSchema

logger = get_logger(__name__)
app = Flask(__name__)
app.config.from_object("app.config.Config")


@app.route("/healthcheck", methods=["GET"])
def hello_world():
    logger.info("healthcheck: Checking database connection")
    session.connection()
    session.close()
    return jsonify({"status": "ok"})


@app.route("/users", methods=["GET", "POST"])
@error_handler
def users():
    if request.method == "GET":
        logger.info("users.request: %s", request)
        users_db = session.query(User).all()
        response = UserSchema().dump(users_db, many=True)
        logger.info("users.response: %s", response)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "POST":
        logger.info("users.request: %s", request)
        validated_request = UserSchema().load(request.json)
        logger.info("users.validated_request: %s", validated_request)

        user = User(**validated_request)
        session.add(user)
        session.commit()

        response = UserSchema().dump(user)
        logger.info("users.response: %s", response)

        return jsonify(response), HTTPStatus.CREATED.value
