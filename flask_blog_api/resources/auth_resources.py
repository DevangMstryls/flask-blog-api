from flask import request
from flask_restful import Resource
from helpers.database import get_db_connection
from schemas.auth import RegisterUserSchema

register_user_schema = RegisterUserSchema()

class RegisterRoute(Resource):
    def post(self, **kwargs):
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
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500
