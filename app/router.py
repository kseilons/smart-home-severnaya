import os
import traceback

import config
from app import app, deviceAdapter, userAdapter

from flask import render_template
from flask import send_from_directory
from flask import jsonify
from flask import request

from app.tokens.token import Token


@app.route('/app/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


# OAuth's entry point
@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    try:
        if request.method == 'GET':
            # Ask user for login and password
            return render_template('login.html')
        elif request.method == 'POST':
            return userAdapter.auth()
    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500


# OAuth, token request
@app.route('/token/', methods=['POST'])
def token():
    try:
        return userAdapter.token()
    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500


# Just placeholder for root
@app.route('/')
def root():
    return "Your smart home is ready."


# Script must response 200 OK on this request
@app.route('/v1.0', methods=['GET', 'POST'])
def main_v10():
    return "OK"


# Method to revoke token
@app.route('/v1.0/user/unlink', methods=['POST'])
def unlink():
    try:
        request_id = request.headers.get('X-Request-Id')
        Token.delete()
        return jsonify({'request_id': request_id})
    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500


# Devices list
@app.route('/v1.0/user/devices', methods=['GET'])
def devices_list():
    try:
        return deviceAdapter.getDevices()

    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500


# Method to query current device status
@app.route('/v1.0/user/devices/query', methods=['POST'])
def query():
    try:
        return deviceAdapter.query()
    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500


# Method to execute some action with devices
@app.route('/v1.0/user/devices/action', methods=['POST'])
def action():
    try:
        return deviceAdapter.action()
    except Exception as ex:
        app.logger.error(traceback.format_exc())
        return f"Error {type(ex).__name__}: {str(ex)}", 500
