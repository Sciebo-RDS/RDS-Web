from __init__ import app
from flask import Blueprint, request, redirect, render_template
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
from src.Util import parseResearch, parseAllResearch, parseResearchBack, parseAllResearchBack, parsePortBack, removeDuplicates
from src.EasierRDS import parseDict
import logging
import functools
import os
import json
import requests
import jwt


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

socketio = SocketIO(
    app, cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS"))
)

socket_blueprint = Blueprint("socket_blueprint", __name__)

clients = {}


url = "https://sciebords-dev2.uni-muenster.de"

data = {
    os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service"): [
        ("getUserServices", "{url}/user/{userId}/service"),
        ("getServicesList", "{url}/service", "get", removeDuplicates),
        ("getService", "{url}/service/{servicename}"),
        ("getServiceForUser", "{url}/user/{userId}/service/{servicename}"),
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


def exchangeCode(data):
    body = {
        'servicename': "port-owncloud",
        'code': data["code"],
        'state': data["state"],
        "userId": current_user.userId
    }

    # TODO exchange it in the background for user and redirect to wizard / projects

    jwtEncode = jwt.encode(body, os.getenv(
        "OWNCLOUD_OAUTH_CLIENT_SECRET"), algorithm="HS256")

    urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service")

    req = requests.post(f"{urlPort}/exchange", json=jwtEncode,
                        verify=os.getenv("VERIFY_SSL", "False") == "True")
    LOGGER.debug(req.text)

    return req


@ socketio.event
def triggerSynchronization(json):
    httpManager.makeRequest("triggerFileSynchronization", data=json)
    httpManager.makeRequest("triggerMetadataSynchronization", data=json)
    httpManager.makeRequest("finishResearch", data=json)


def authenticated_only(f):
    @ functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            logout_user()
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@ socketio.on("connect")
def connected():
    LOGGER.info("connected")

    if current_user.is_authenticated:
        current_user.websocketId = request.sid
        clients[current_user.userId] = current_user

        emit("ServiceList", httpManager.makeRequest("getServicesList"))
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))
    else:
        logout_user()
        disconnect()


@ socketio.on("disconnect")
def disconnect():
    LOGGER.info("disconnected")

    del clients[current_user.userId]
    logout_user()


@ socketio.on("sendMessage")
@ authenticated_only
def handle_message(jsonData):
    LOGGER.info("got {}".format(jsonData))
    emit("getMessage", {"message": jsonData["message"][::-1]}, json=True)


@socketio.on("addCredentials")
@authenticated_only
def credentials(jsonData):
    jsonData = json.loads(jsonData)

    body = {
        "servicename": jsonData["servicename"],
        "username": jsonData["username"],
        "password": jsonData["password"],
        "userId": current_user.userId
    }

    if not body["username"]:
        body["username"] = "---"

    urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service")
    req = requests.post(f"{urlPort}/credentials", json=body,
                        verify=os.getenv("VERIFY_SSL", "False") == "True")
    LOGGER.debug(req.text)

    # update userserviceslist on client
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))

    return req.status_code < 300


@socketio.on("exchangeCode")
@authenticated_only
def exchangeCode(jsonData):
    jsonData = json.loads(jsonData)

    req = exchangeCode(jsonData)
    LOGGER.debug(req.text)

    # update userserviceslist on client
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))

    return req.status_code < 300
