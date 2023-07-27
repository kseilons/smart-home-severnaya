import json
import os

from flask import request
from app import app


def get_user(user_id):
    request.user_id = user_id
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, 'data', user_id + ".json")
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        with open(filename, mode='r') as f:
            text = f.read()
            data = json.loads(text)
            return data
    else:
        app.logger.warning(f"user not found")
        return None
