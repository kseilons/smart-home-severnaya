import os

from flask import request
from app import app
from utils.generate import random_string


class Token:
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


    # Function to retrieve token from header
    @staticmethod
    def getTokenFromReq():
        try:
            prefix, token = request.headers.get('Authorization').split(' ', 2)
        except ValueError:
            app.logger.warning(f"invalid token: {request.headers.get('Authorization')}")
            return None

        if prefix.lower() == 'bearer':
            return token
        else:
            app.logger.warning(f"invalid token prefix: {prefix}")
            return None

    # Function to check current token, returns username
    @classmethod
    def get_id(cls):
        access_token_file = os.path.join(cls.token_path, cls.getTokenFromReq())
        if os.path.exists(access_token_file):
            with open(access_token_file, 'r') as f:
                request.user_id = f.read()
                return request.user_id
        return None

    # Generate and save random token with username
    @classmethod
    def create(cls, code):
        access_token = random_string(32)
        access_token_file = os.path.join(cls.token_path, access_token)
        with open(access_token_file, mode='wb') as f:
            f.write(code.encode('utf-8'))
        return access_token

    @classmethod
    def delete(cls):
        access_token = cls.getTokenFromReq()
        access_token_file = os.path.join(cls.token_path, access_token)
        if os.path.isfile(access_token_file) and os.access(access_token_file, os.R_OK):
            os.remove(access_token_file)
            app.logger.info(f"token {access_token} revoked")



