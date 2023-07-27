import urllib
from time import time

from flask import request, render_template, redirect, jsonify

import config
from app import app
from app.tokens.token import Token
from app.users.user import get_user
from utils.generate import random_string



class UserAdapter:
    last_code = None
    last_code_user = None
    last_code_time = None
    @classmethod
    def auth(cls):
        cls.last_code_user = request.form["username"]
        cls.last_code_time = time()
        if ("username" not in request.form
                or "password" not in request.form
                or "state" not in request.args
                or "response_type" not in request.args
                or request.args["response_type"] != "code"
                or "client_id" not in request.args
                or request.args["client_id"] != config.YandexClient.IDAPP):
            if "username" in request.form:
                request.user_id = request.form['username']
            app.logger.error("invalid auth request")
            return "Invalid request", 400
        # Check login and password
        user = get_user(request.form["username"])
        if user == None or user["password"] != request.form["password"]:
            app.logger.warning("invalid password")
            return render_template('login.html', login_failed=True)

        # Generate random code and remember this user and time
        cls.last_code = random_string(8)


        params = {'state': request.args['state'],
                  'code': cls.last_code,
                  'client_id': config.YandexClient.IDAPP}
        app.logger.info(f"code generated, {cls.last_code}")
        return redirect(request.args["redirect_uri"] + '?' + urllib.parse.urlencode(params))

    @classmethod
    def token(cls):
        request.user_id = cls.last_code_user
        if ("client_secret" not in request.form
                or request.form["client_secret"] != config.YandexClient.SECRET
                or "client_id" not in request.form
                or request.form["client_id"] != config.YandexClient.IDAPP
                or "code" not in request.form):
            app.logger.error("invalid token request")
            return "Invalid request", 400
        # Check code
        if request.form["code"] != cls.last_code:
            app.logger.warning(f'invalid code. В запросе: {request.form["code"]}. последний {cls.last_code}')
            return "Invalid code", 403
        # Check time
        if time() - cls.last_code_time > 10:
            app.logger.warning("code is too old")
            return "Code is too old", 403

        access_token = Token.create(cls.last_code_user)
        app.logger.info("access granted")
        # Return just token without any expiration time
        return jsonify({'access_token': access_token})