from flask import render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from flask_socketio import SocketIO
from __init__ import app
from websocket import socket_blueprint, socketio
import requests
import uuid
import os
import logging
import json
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
CORS(app, origins=json.loads(os.getenv("FLASK_ORIGINS")))

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

login_manager = LoginManager()

# temporary user_store
user_store = {}

login_manager.init_app(app)
login_manager.login_view = "index"
app.register_blueprint(socket_blueprint)


class User(UserMixin):
    def __init__(self, id, userId, websocketId=None, token=None):
        super().__init__()
        self.id = id
        self.userId = userId
        self.websocketId = websocketId


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


@ app.route("/")
def index():
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
            return render_template("exchangeCode.html")

        return render_template("index.html")

    return redirect(
        os.getenv(
            "REDIRECTION_URL",
            "https://10.14.29.60/owncloud/index.php/apps/oauth2/authorize?response_type=token&client_id=Pb0UGAlNBx0Hr35mhd5DSt0jBpg1YbApwn7Hf61nREiXinZT3ucVg9K1RSKuW4Di&redirect_uri=http://localhost:8080/",
        )
    )


@ login_manager.user_loader
def load_user(user_id):
    return user_store.get(user_id)


@ app.route("/logout")
@ login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)
