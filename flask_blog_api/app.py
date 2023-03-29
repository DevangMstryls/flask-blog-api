import os

from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_restful import Api
from middlewares.authentication_middleware import AuthenticationMiddleware
from resources.auth_resources import LoginRoute, RegisterRoute
from resources.blog_resources import (AllBlogPostsRoute, BlogPostRoute,
                                      CreateBlogPostRoute)

load_dotenv(verbose=True)

env = os.getenv('ENV')

print(env)

app = Flask(__name__)

# define all your blueprints here
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


api = Api(auth_bp)
posts_api = Api(posts_bp)


# Register Routes
api.add_resource(RegisterRoute, '/register')
api.add_resource(LoginRoute, '/login')

posts_api.add_resource(CreateBlogPostRoute, '/create')
posts_api.add_resource(BlogPostRoute, '/<int:post_id>')
posts_api.add_resource(AllBlogPostsRoute, '/')

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)


app.wsgi_app = AuthenticationMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
