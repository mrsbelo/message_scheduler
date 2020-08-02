from http import HTTPStatus

from flask import Flask, jsonify, request

from .clients import check_if_message_exists, is_user_ok_to_recieve_this_kind
from .db import session
from .decorators import error_handler
from .logs import get_logger
from .models import Message, User
from .schemas import MessageSchema, UserSchema

logger = get_logger(__name__)
app = Flask(__name__)
app.config.from_object("app.config.Config")


@app.route("/healthcheck", methods=["GET"])
def hello_world():
    logger.info("healthcheck: Checking database connection")
    session.connection()
    session.close()

    return jsonify({"status": "ok"}), HTTPStatus.OK.value


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


@app.route("/users/<int:user_id>", methods=["GET", "DELETE", "PUT"])
@error_handler
def users_detail(user_id):
    if request.method == "GET":
        logger.info("users.request: %s", request)
        logger.info("users.user_id: %s", user_id)
        user_db = session.query(User).get(user_id)
        if not user_db:
            response = {"message": "User not found"}
            return jsonify(response), HTTPStatus.NOT_FOUND.value

        response = UserSchema().dump(user_db)
        logger.info("users.response: %s", response)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "PUT":
        logger.info("users.request: %s", request)
        logger.info("users.user_id: %s", user_id)
        user_db = session.query(User).get(user_id)
        if not user_db:
            response = {"message": "User not found"}
            return jsonify(response), HTTPStatus.NOT_FOUND.value

        validated_request = UserSchema().load(request.json)
        for key, value in validated_request.items():
            setattr(user_db, key, value)

        session.add(user_db)
        session.commit()

        response = UserSchema().dump(user_db)
        logger.info("users.response: %s", response)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "DELETE":
        logger.info("users.request: %s", request)
        logger.info("users.user_id: %s", user_id)
        user_db = session.query(User).get(user_id)
        if not user_db:
            response = {"message": "User not found"}
            return jsonify(response), HTTPStatus.NOT_FOUND.value

        session.delete(user_db)
        session.commit()
        logger.info("user.deleted")

        return jsonify({}), HTTPStatus.NO_CONTENT.value


@app.route("/messages", methods=["GET", "POST"])
@error_handler
def messages():
    if request.method == "GET":
        logger.info("messages.request: %s", request)
        messages_db = session.query(Message).all()
        response = MessageSchema().dump(messages_db, many=True)
        logger.info("messages.response: %s", response)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "POST":
        logger.info("messages.request: %s", request)
        validated_request = MessageSchema().load(request.json)
        logger.info("messages.validated_request: %s", validated_request)

        if check_if_message_exists(validated_request):
            response = {"message": "This message is already registered"}

            return jsonify(response), HTTPStatus.OK.value

        if not is_user_ok_to_recieve_this_kind(validated_request):
            response = {
                "message": "User cant recieve this message, user register is incomplete"
            }

            return jsonify(response), HTTPStatus.OK.value

        message = Message(**validated_request)
        session.add(message)
        session.commit()

        response = MessageSchema().dump(message)
        logger.info("messages.response: %s", response)

        return jsonify(response), HTTPStatus.CREATED.value


@app.route("/messages/<int:message_id>", methods=["GET", "DELETE"])
@error_handler
def messages_detail(message_id):
    if request.method == "GET":
        logger.info("messages.request: %s", request)
        logger.info("messages.message_id: %s", message_id)
        message_db = session.query(Message).get(message_id)
        if not message_db:
            response = {"message": "Message not found"}
            return jsonify(response), HTTPStatus.NOT_FOUND.value

        response = MessageSchema().dump(message_db)
        logger.info("messages.response: %s", response)

        return jsonify(response), HTTPStatus.OK.value

    elif request.method == "DELETE":
        logger.info("messages.request: %s", request)
        logger.info("messages.message_id: %s", message_id)
        message_db = session.query(Message).get(message_id)
        if not message_db:
            response = {"message": "Message not found"}
            return jsonify(response), HTTPStatus.NOT_FOUND.value

        session.delete(message_db)
        session.commit()
        logger.info("message.deleted")

        return jsonify({}), HTTPStatus.NO_CONTENT.value


@app.route("/", defaults={"path": ""})
@app.route(
    "/<path:path>",
    methods=[
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
    ],
)
@error_handler
def page_not_found(path):
    """Capture everything and throws 404 Page not found"""
    return jsonify({"message": "Page not found"}), HTTPStatus.NOT_FOUND.value
