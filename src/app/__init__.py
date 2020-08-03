from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_cors import CORS

from .db import session
from .decorators import error_handler
from .logs import get_logger
from .models import Message, User
from .schemas import MessageSchema, UserSchema
from .views_functions import (
    add_a_message_schedule,
    add_a_user,
    generic_delete_method,
    generic_get_detail_method,
    generic_get_list_method,
    update_a_user,
)

logger = get_logger(__name__)
app = Flask(__name__)
CORS(app)
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
        return generic_get_list_method(User, request, UserSchema)

    elif request.method == "POST":
        return add_a_user(request)


@app.route("/users/<int:user_id>", methods=["GET", "DELETE", "PUT"])
@error_handler
def users_detail(user_id):
    if request.method == "GET":
        return generic_get_detail_method(user_id, User, request, UserSchema)

    elif request.method == "PUT":
        return update_a_user(request, user_id)

    elif request.method == "DELETE":
        return generic_delete_method(user_id, User, request)


@app.route("/messages", methods=["GET", "POST"])
@error_handler
def messages():
    if request.method == "GET":
        return generic_get_list_method(Message, request, MessageSchema)

    elif request.method == "POST":
        return add_a_message_schedule(request)


@app.route("/messages/<int:message_id>", methods=["GET", "DELETE"])
@error_handler
def messages_detail(message_id):
    if request.method == "GET":
        return generic_get_detail_method(message_id, Message, request, MessageSchema)

    elif request.method == "DELETE":
        return generic_delete_method(message_id, Message, request)


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
