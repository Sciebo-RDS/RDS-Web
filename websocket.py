from __init__ import app
from flask import Blueprint, request, redirect
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
import logging
import functools
import os
from server.EasierRDS import HTTPManager, HTTPRequest


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

socketio = SocketIO(
    app, cors_allowed_origins=[
        "http://localhost:8085", "http://localhost:8080"]
)

socket_blueprint = Blueprint("socket_blueprint", __name__)

clients = {}


def addJwtWithUser(response):
    # here needs to make the response into a jwt and
    return response


def parseJwtAndCheckIfAllCorrect(response):
    # check here, if the jwt is correct and take the username out of it and check against logged in user.
    return response


http = HTTPRequest(os.getenv("CIRCLE2_PORT_SERVICE",
                             "https://sciebords-dev2.uni-muenster.de/port-service"))
http.addRequest("getServicesList", "{url}/service", "get", addJwtWithUser)
http.addRequest("getUserServices", "{url}/user/{userId}/service")
http.addRequest("getService", "{url}/service/{servicename}")
http.addRequest("getServiceForUser",
                "{url}/user/{userId}/service/{servicename}")
http.addRequest("addServiceForUser",
                "{url}/exchange", "post", parseJwtAndCheckIfAllCorrect)  # add here the jwt security stuff from php
http.addRequest("removeServiceForUser",
                "{url}/user/{userId}/service/{servicename}", "delete")

httpResearch = HTTPRequest(os.getenv("CIRCLE2_EXPORTER_SERVICE",
                                     "https://sciebords-dev2.uni-muenster.de/exporter"))
httpResearch.addRequest(
    "addImport", "{url}/user/{userId}/research/{researchId}/imports")

httpManager = HTTPManager(socketio)
httpManager.addService(http)
httpManager.addService(httpResearch)


def authenticated_only(f):
    @ functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not __name__ == "__main__" and not current_user.is_authenticated:
            logout_user()
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on("connect")
def connected():
    LOGGER.info("connected")

    if __name__ == "__main__":
        return

    if current_user.is_authenticated:
        current_user.websocketId = request.sid
        clients[current_user.userId] = current_user
    else:
        logout_user()
        disconnect()


@socketio.on("disconnect")
def disconnect():
    LOGGER.info("disconnected")

    if __name__ == "__main__":
        return

    del clients[current_user.userId]
    logout_user()


@socketio.on("sendMessage")
@authenticated_only
def handle_message(json):
    LOGGER.info("got {}".format(json))
    emit("getMessage", {"message": json["message"][::-1]}, json=True)


if __name__ == "__main__":

    @app.route("/")
    def index():
        return redirect("http://localhost:8085")

    app.register_blueprint(socket_blueprint)
    socketio.run(app, debug=True, port=8080)
