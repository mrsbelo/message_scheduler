from marshmallow import EXCLUDE, Schema
from marshmallow.fields import Email, Integer, String


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class UserSchema(BaseSchema):
    class Meta:
        include = {"id": Integer(dump_only=True)}

    name = String(required=True)
    email = Email()
    phone = String()
