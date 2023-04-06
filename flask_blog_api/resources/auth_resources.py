from flask import request
from flask_restful import Resource
from helpers.database import get_db_connection
from helpers.utils import (generate_auth_token, get_hashed_password,
                           password_matches)
from marshmallow import ValidationError
from schemas.auth import (LoggedInUserSchema, LoginSchema, RegisterUserSchema,
                          UserSchema)

register_user_schema = RegisterUserSchema()
login_schema = LoginSchema()
user_schema = UserSchema()
logged_in_user_schema = LoggedInUserSchema()

class RegisterRoute(Resource):
    def post(self):
        try:
            payload = request.get_json(force=True)

            data = register_user_schema.load(payload)

            db_conn = get_db_connection()
            user = db_conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (data['email'],)
            ).fetchone()

            if user:
                return {
                    'success': False,
                    'error': 'User with that email already exists'
                }, 400

            name = data['name']
            email = data['email']
            password = get_hashed_password(data['password'])
            token = generate_auth_token()

            db_conn.execute(
                "INSERT INTO users (name, email, password, token) VALUES (?, ?, ?, ?)",
                (name, email, password, token)
            )

            db_conn.commit()
            db_conn.close()

            return {
                'success': True,
            }, 200
        except ValidationError as e:
            return {
                'success': False,
                'error': e.messages,
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500


class LoginRoute(Resource):
    def post(self):
        try:
            payload = request.get_json(force=True)

            data = login_schema.load(payload)

            email = data['email']
            password = data['password']

            db_conn = get_db_connection()
            user = db_conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()
            db_conn.close()

            user_obj = logged_in_user_schema.dump(user)

            # validations
            if user is None:
                return {
                    'success': False,
                    'error': 'User does not exists'
                }, 404
            
            if password_matches(password, user_obj['password']):
                return {
                    'success': False,
                    'error': 'Incorrect password'
                }, 401

            return {
                'success': True,
                'data': user_obj,
            }, 200
        except ValidationError as e:
            return {
                'success': False,
                'error': e.messages,
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500
