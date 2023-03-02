from marshmallow import Schema, fields


class RegisterUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_on = fields.DateTime()
