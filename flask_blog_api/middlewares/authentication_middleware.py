import datetime
import json

from helpers.utils import get_token_from_request
from werkzeug.wrappers import Request, Response

authenticated_request_paths = [
    '/create',
]

unauthenticated_request_paths = [
    '/'
]


class AuthenticationMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, resp):

        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)
        request_path = request.path

        # By pass OPTIONS request from checking for authentication; fixed for website /questions
        # ref: https://cloud.google.com/functions/docs/writing/http#limitations
        if request.method != 'OPTIONS' and \
            request_path not in unauthenticated_request_paths and \
            any(rp in request_path for rp in authenticated_request_paths):

            # token validation
            request_token = get_token_from_request(request)
            if not request_token:
                res = Response(
                    json.dumps({
                        'success': False,
                        'error': 'Unauthorized access'
                    }),
                    status=401,
                    mimetype="application/json",
                )

                return res(environ, resp)

        return self.app(environ, resp)
