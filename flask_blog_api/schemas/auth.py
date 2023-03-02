from marshmallow import Schema, fields


class RegisterUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Email(required=True)
    