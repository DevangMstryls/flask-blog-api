from flask import request
from flask_restful import Resource


class RegisterRoute(Resource):
    def post(self, **kwargs):
        payload = request.get_json(force=True)

        

        return {
            'success': True,
        }, 200
