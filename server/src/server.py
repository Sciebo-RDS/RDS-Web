from flask_cors import CORS
from flask import Response, stream_with_context
from flask import render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from .app import app, socketio, user_store, development_mode
from .websocket import socket_blueprint, exchangeCode
import json
import requests
import uuid
import os
import logging
import uuid
import os

CORS(app, origins=json.loads(os.getenv("FLASK_ORIGINS")))

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
app.register_blueprint(socket_blueprint)


def proxy(host, path):
    req = requests.get(f"{host}{path}", stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type=req.headers['content-type'])


class User(UserMixin):
    def __init__(self, id, userId, websocketId=None, token=None):
        super().__init__()
        self.id = id
        self.userId = userId
        self.websocketId = websocketId


@app.route("/informations")
def informations():
    data = {}

    redirectUrl = os.getenv("VUE_APP_REDIRECTION_URL")
    if redirectUrl is not None:
        data["redirectUrl"] = redirectUrl

    return json.dumps(data)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return "", 200
        else:
            "", 401

    if "access_token" in request.args:
        token = request.args["access_token"]
        headers = {"Authorization": "Bearer {}".format(token)}
        req = requests.get(
            "{}/index.php/apps/rds/informations".format(
                os.getenv("CHECK_URL", "https://10.14.29.60/owncloud")
            ),
            headers=headers,
            verify=False,
        )

        if req.status_code == 200:
            data = req.json()
            user = User(
                id=uuid.uuid4(), userId=data["username"], websocketId=None, token=token
            )
            user_store[user.get_id()] = user
            login_user(user)

            return "", 200

    return "", 401


@ login_manager.user_loader
def load_user(user_id):
    return user_store.get(user_id)


@ app.route("/logout")
@ login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def index(path):
    if development_mode and os.getenv("VUE_APP_SKIP_REDIRECTION", "False") == "True":
        LOGGER.debug("skip authentication")
        user = User(
            id=uuid.uuid4(), userId=os.getenv("DEV_FLASK_USERID"), websocketId=None, token=None
        )
        user_store[user.get_id()] = user
        login_user(user)
        return proxy(os.getenv("DEV_WEBPACK_DEV_SERVER_HOST"), request.path)

    if "access_token" in request.args:
        token = request.args["access_token"]
        headers = {"Authorization": "Bearer {}".format(token)}
        req = requests.get(
            "{}/index.php/apps/rds/informations".format(
                os.getenv("CHECK_URL", "https://10.14.29.60/owncloud")
            ),
            headers=headers,
            verify=False,
        )

        if req.status_code == 200:
            data = req.json()
            user = User(
                id=uuid.uuid4(), userId=data["username"], websocketId=None, token=token
            )
            user_store[user.get_id()] = user
            login_user(user)
            return redirect("/")

    if current_user.is_authenticated:
        if "code" in request.args and "state" in request.args:
            exchangeCode(request.args)
            return render_template("exchangeCode.html")

        if development_mode:
            LOGGER.debug("path: {}".format(request.path))
            return proxy(os.getenv("DEV_WEBPACK_DEV_SERVER_HOST"), request.path)

        return app.send_static_file(path)

    return redirect(
        os.getenv("VUE_APP_REDIRECTION_URL")
    )
