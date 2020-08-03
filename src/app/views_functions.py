from http import HTTPStatus

from flask import jsonify

from .clients import (
    check_if_message_exists,
    get_user_by_id,
    is_user_ok_to_recieve_this_kind,
)
from .db import session
from .logs import get_logger
from .models import Message, User
from .schemas import MessageSchema, UserSchema

logger = get_logger(__name__)


def generic_delete_method(instance_id, model, request):
    logger.info("request: %s", request)
    logger.info("instance_id: %s", instance_id)
    instance_db = session.query(model).get(instance_id)
    if not instance_db:
        response = {"message": f"{model.__tablename__.capitalize()} not found"}
        return jsonify(response), HTTPStatus.NOT_FOUND.value

    session.delete(instance_db)
    session.commit()
    logger.info("user.deleted")

    return jsonify({}), HTTPStatus.NO_CONTENT.value


def generic_get_detail_method(instance_id, model, request, schema):
    logger.info("request: %s", request)
    logger.info("instance_id: %s", instance_id)
    instance_db = session.query(model).get(instance_id)
    if not instance_db:
        response = {"message": f"{model.__tablename__.capitalize()} not found"}
        return jsonify(response), HTTPStatus.NOT_FOUND.value

    response = schema().dump(instance_db)
    logger.info("response: %s", response)

    return jsonify(response), HTTPStatus.OK.value


def generic_get_list_method(model, request, schema):
    logger.info("request: %s", request)
    instances_db = session.query(model).all()
    response = schema().dump(instances_db, many=True)
    logger.info("response: %s", response)

    return jsonify(response), HTTPStatus.OK.value


def add_a_user(request):
    logger.info("request: %s", request)
    validated_request = UserSchema().load(request.json)
    logger.info("validated_request: %s", validated_request)

    user = User(**validated_request)
    session.add(user)
    session.commit()

    response = UserSchema().dump(user)
    logger.info("response: %s", response)

    return jsonify(response), HTTPStatus.CREATED.value


def update_a_user(request, user_id):
    logger.info("request: %s", request)
    logger.info("user_id: %s", user_id)
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
    logger.info("response: %s", response)

    return jsonify(response), HTTPStatus.OK.value


def add_a_message_schedule(request):
    logger.info("request: %s", request)
    validated_request = MessageSchema().load(request.json)
    logger.info("validated_request: %s", validated_request)

    if check_if_message_exists(validated_request):
        response = {"message": "This message is already registered"}

        return jsonify(response), HTTPStatus.OK.value

    user_db = get_user_by_id(validated_request["user_id"])
    if not user_db:
        response = {"message": "user_id not found"}

        return jsonify(response), HTTPStatus.BAD_REQUEST.value

    if not is_user_ok_to_recieve_this_kind(user_db, validated_request):
        response = {
            "message": "User cant recieve this message, user register is incomplete"
        }

        return jsonify(response), HTTPStatus.OK.value

    message = Message(**validated_request)
    session.add(message)
    session.commit()

    response = MessageSchema().dump(message)
    logger.info("response: %s", response)

    return jsonify(response), HTTPStatus.CREATED.value
