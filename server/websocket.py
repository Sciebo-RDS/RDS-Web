from __init__ import app
from flask import Blueprint, request, redirect
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
from src.Util import parseResearch, parseAllResearch, parseResearchBack, parseAllResearchBack, parsePortBack
from src.EasierRDS import parseDict
import logging
import functools
import os
import json


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

socketio = SocketIO(
    app, cors_allowed_origins=[
        "http://localhost:8085", "http://localhost:8080"]
)

socket_blueprint = Blueprint("socket_blueprint", __name__)

clients = {}


url = "https://sciebords-dev2.uni-muenster.de"

data = {
    os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service"): [
        ("getUserServices", "{url}/user/{userId}/service"),
        ("getServicesList", "{url}/service"),
        ("getService", "{url}/service/{servicename}"),
        ("getServiceForUser", "{url}/user/{userId}/service/{servicename}"),
        ("addServiceForUser", "{url}/exchange", "post"),
        ("removeServiceForUser",
         "{url}/user/{userId}/service/{servicename}", "delete")
    ],
    os.getenv("USE_CASE_SERVICE_EXPORTER_SERVICE", f"{url}/exporter"): [
        ("getAllFiles", "{url}/user/{userId}/research/{researchId}"),
        ("triggerFileSynchronization",
         "{url}/user/{userId}/research/{researchId}", "post"),
        ("removeAllFiles",
         "{url}/user/{userId}/research/{researchId}", "delete")
    ],
    os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"): [
        ("getAllResearch", "{url}/user/{userId}", "get", parseAllResearch),
        ("getResearch",
         "{url}/user/{userId}/research/{researchId}", "get", parseResearch),
        ("createResearch", "{url}/user/{userId}", "post"),
        ("removeAllResearch", "{url}/user/{userId}", "delete"),
        ("removeResearch",
         "{url}/user/{userId}/research/{researchId}", "delete"),
        ("addImport",
         "{url}/user/{userId}/research/{researchId}/imports", "post", parsePortBack),
        ("addExport",
         "{url}/user/{userId}/research/{researchId}/exports", "post", parsePortBack),
        ("removeImport",
         "{url}/user/{userId}/research/{researchId}/imports/{portId}", "delete"),
        ("removeExport",
         "{url}/user/{userId}/research/{researchId}/exports/{portId}", "delete")
    ],
    os.getenv("USE_CASE_SERVICE_METADATA_SERVICE", f"{url}/metadata"): [
        ("finishResearch", "{url}/user/{userId}/research/{researchId}", "put"),
        ("triggerMetadataSynchronization",
         "{url}/user/{userId}/research/{researchId}", "patch")
    ]
}

httpManager = parseDict(data, socketio=socketio)


@ socketio.event
def triggerSynchronization(json):
    httpManager.makeRequest("triggerFileSynchronization", data=json)
    httpManager.makeRequest("triggerMetadataSynchronization", data=json)
    httpManager.makeRequest("finishResearch", data=json)


def authenticated_only(f):
    @ functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not __name__ == "__main__" and not current_user.is_authenticated:
            logout_user()
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@ socketio.on("connect")
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


@ socketio.on("disconnect")
def disconnect():
    LOGGER.info("disconnected")

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

    @ app.route("/")
    def index():
        return redirect("http://localhost:8085")

    app.register_blueprint(socket_blueprint)
    socketio.run(app, debug=True, port=8080)
