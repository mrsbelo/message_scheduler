from http import HTTPStatus

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .logs import get_logger

logger = get_logger(__name__)


def error_handler(func):
    def _error_handler(**kwargs):
        try:
            return func(**kwargs)
        except ValidationError as exc:
            logger.info("ValidationError: %s", exc)
            json_response = json.dumps(exc.messages)

            return jsonify(json_response), HTTPStatus.BAD_REQUEST.value

        except IntegrityError as exc:
            logger.info("IntegrityError: %s", exc)
            json_response = {"message": exc.args[0]}

            return jsonify(json_response), HTTPStatus.BAD_REQUEST.value

        except Exception as exc:
            logger.info("Internal server error: %s", exc)
            json_response = {"message": "Internal server error"}

            return jsonify(json_response), HTTPStatus.INTERNAL_SERVER_ERROR.value

    return _error_handler
