import os

from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_restful import Api
from resources.auth_resources import LoginRoute, RegisterRoute

load_dotenv(verbose=True)

env = os.getenv('ENV')

print(env)

app = Flask(__name__)

# define all your blueprints here
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


api = Api(auth_bp)


# Register Routes
api.add_resource(RegisterRoute, '/register')
api.add_resource(LoginRoute, '/login')

app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
