from __init__ import app
from flask import Blueprint, request, redirect
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
import logging
import functools


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

socketio = SocketIO(
    app, cors_allowed_origins=[
        "http://localhost:8085", "http://localhost:8080"]
)

socket_blueprint = Blueprint("socket_blueprint", __name__)

clients = {}


def authenticated_only(f):
    @ functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not __name__ == "__main__" and not current_user.is_authenticated:
            logout_user()
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


servicelist = []


@socketio.on("addService")
@authenticated_only
def addService(json):
    LOGGER.info(json)
    if json["service"] not in servicelist:
        servicelist.append(json["service"])
    LOGGER.info(servicelist)


@socketio.on("requestServiceList")
@authenticated_only
def requestServiceList():
    LOGGER.info(servicelist)
    emit("ServiceList", {"list": servicelist}, json=True)


@ socketio.on("connect")
def connected():
    LOGGER.info("{} connected")

    if __name__ == "__main__":
        return

    if current_user.is_authenticated:
        current_user.websocketId = request.sid
        clients[current_user.userId] = current_user
    else:
        logout_user()
        disconnect()


@ socketio.on("disconnect")
def disconnect():
    LOGGER.info("{} disconnected")

    if __name__ == "__main__":
        return

    del clients[current_user.userId]
    logout_user()


@ socketio.on("sendMessage")
@ authenticated_only
def handle_message(json):
    LOGGER.info("got {}".format(json))
    emit("getMessage", {"message": json["message"][::-1]}, json=True)


if __name__ == "__main__":

    @app.route("/")
    def index():
        return redirect("http://localhost:8085")

    app.register_blueprint(socket_blueprint)
    socketio.run(app, debug=True, port=8080)

else:
    pass
