from flask import request
from flask_restful import Resource
from helpers.database import get_db_connection
from marshmallow import ValidationError
from schemas.auth import LoginSchema, RegisterUserSchema, UserSchema

register_user_schema = RegisterUserSchema()
login_schema = LoginSchema()
user_schema = UserSchema()

class RegisterRoute(Resource):
    def post(self):
        try:
            payload = request.get_json(force=True)

            data = register_user_schema.load(payload)

            name = data['name']
            email = data['email']
            password = data['password']

            db_conn = get_db_connection()
            db_conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
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

            # validations
            if user is None:
                return {
                    'success': False,
                    'error': 'User does not exists'
                }, 404
            
            if user['password'] != password:
                return {
                    'success': False,
                    'error': 'Incorrect password'
                }, 401
            
            result = user_schema.dump(user)

            return {
                'success': True,
                'data': result,
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
