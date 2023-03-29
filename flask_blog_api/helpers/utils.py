import secrets

import bcrypt


def get_token_from_request(req):
    auth_token_header = req.headers.get('authorization')
    if auth_token_header:
        return auth_token_header.replace('Bearer ', '')
    return None

def generate_auth_token():
    # Generate a 32-byte random token
    token = secrets.token_bytes(32)
    # Convert the token to a hexadecimal string
    return  token.hex()

# Generate a salt for the password
salt = bcrypt.gensalt()

def get_hashed_password(password):
    # Encrypt a password using the salt
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def password_matches(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
