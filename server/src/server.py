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
import jwt

CORS(app, origins=json.loads(os.getenv("FLASK_ORIGINS")), supports_credentials=True)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
app.register_blueprint(socket_blueprint)

req = requests.get(
    "{}/apps/rds/publickey".format(
        os.getenv("OWNCLOUD_URL",
                  "https://10.14.29.60/owncloud/index.php")
    ),
    verify=os.getenv("VERIFY_SSL", "False") == "True"
).json()

publickey = req.get("publickey", "").replace("\\n", "\n")


def proxy(host, path):
    req = requests.get(f"{host}{path}", stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type=req.headers['content-type'])


class User(UserMixin):
    def __init__(self, id, userId=None, websocketId=None, token=None):
        super().__init__()
        self.id = id
        self.websocketId = websocketId
        self.userId = userId
        self.token = token

        if userId is None:
            headers = {
                "Authorization": f"Bearer {token}"
            }

            req = requests.get(
                "{}/apps/rds/informations".format(
                    os.getenv("OWNCLOUD_URL",
                              "https://10.14.29.60/owncloud/index.php")
                ),
                headers=headers,
                verify=os.getenv("VERIFY_SSL", "False") == "True",
            )

            if req.status_code == 200:
                text = req.json()["jwt"]

                data = jwt.decode(
                    text, publickey, algorithms=["RS256"]
                )
                LOGGER.debug(data)

                self.userId = data["username"]
                return
            raise ValueError


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
        return ("", 200) if (current_user.is_authenticated) else ("", 401)

    reqData = request.get_json(force=True)
    LOGGER.debug("reqdata: {}".format(reqData))

    user = None
    if publickey != "":
        try:
            decoded = jwt.decode(
                reqData["informations"], publickey, algorithms=["RS256"]
            )

            user = User(
                id=uuid.uuid4(),
                userId=decoded["username"]
            )
        except Exception as e:
            LOGGER.error(e, exc_info=True)

    if "Authorization" in request.headers:
        try:
            # TODO: Add check for auth token against owncloud web
            user = User(
                id=uuid.uuid4(),
                token=request.headers["Authorization"].replace(
                    "Bearer ", "").replace("token ", "")
            )
        except Exception as e:
            LOGGER.error(e, exc_info=True)

    if user is not None:
        user_store[user.get_id()] = user
        login_user(user)
        LOGGER.info("logged? {}".format(current_user.is_authenticated))

        LOGGER.debug(user_store)

        return "", 201

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
            id=uuid.uuid4(), userId=os.getenv("DEV_FLASK_USERID")
        )
        user_store[user.get_id()] = user
        login_user(user)
        return proxy(os.getenv("DEV_WEBPACK_DEV_SERVER_HOST"), request.path)

    try:
        user = User(
            id=uuid.uuid4(),
            token=request.args["access_token"]
        )
        user_store[user.get_id()] = user
        login_user(user)
        return redirect("/")
    except Exception as e:
        LOGGER.error(e, exc_info=True)

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
