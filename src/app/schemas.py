from datetime import datetime

from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    post_dump,
    post_load,
    validates,
)
from marshmallow.fields import DateTime, Email, Integer, String
from marshmallow.validate import OneOf

from .constants import DATETIME_FORMAT, KIND_MAP, STATUS_MAP
from .logs import get_logger

logger = get_logger(__name__)


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        include = {"id": Integer(dump_only=True)}

    name = String(required=True)
    email = Email()
    phone = String()


class MessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    created = DateTime(DATETIME_FORMAT, dump_only=True)
    scheduled = DateTime(DATETIME_FORMAT, required=True)
    text = String(required=True)
    kind = String(required=True, validate=[OneOf(["email", "sms", "push", "whatsapp"])])
    status = String(validate=OneOf(["scheduled", "sended"]), missing="scheduled")
    user_id = Integer(required=True)

    @validates("scheduled")
    def cannot_schedule_into_past(self, scheduled, **kwargs):
        if datetime.utcnow() >= scheduled:
            raise ValidationError(
                message="Cannot scheduled messages into the past", field="scheduled"
            )

        return scheduled

    @post_load
    def mapping_kind_and_status_str_to_int_load(self, data, **kwargs):
        if data.get("status"):
            data["status"] = STATUS_MAP[data["status"]]
        data["kind"] = KIND_MAP[data["kind"]]
        return data

    @post_dump
    def mapping_kind_and_status_str_to_int_dump(self, data, **kwargs):
        data["status"] = STATUS_MAP[int(data["status"])]
        data["kind"] = KIND_MAP[int(data["kind"])]

        return data

    @post_load
    def insert_created_field(self, data, **kwargs):
        if not data.get("created"):
            data["created"] = datetime.utcnow().replace(microsecond=0)

        return data
