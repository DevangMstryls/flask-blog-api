from app import api

from flask_blog_api.resources.auth_resources import RegisterRoute


def register_resources():
    # pass
    api.add_resource(RegisterRoute, '/register')
    # api.add_resource(RegisterResource, '/login')
