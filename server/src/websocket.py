from flask import Blueprint, request, redirect, render_template
from flask_socketio import send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
from .Util import parseResearch, parseAllResearch, parseResearchBack, parseAllResearchBack, parsePortBack, removeDuplicates
from .EasierRDS import parseDict
from .app import socketio, clients
import logging
import functools
import os
import json
import requests
import jwt

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


socket_blueprint = Blueprint("socket_blueprint", __name__)


def refreshUserServices():
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))


def refreshProjects():
    emit("ProjectList", httpManager.makeRequest("getAllResearch"))


url = "https://sciebords-dev2.uni-muenster.de"

data = {
    os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service"): [
        ("getUserServices", "{url}/user/{userId}/service"),
        ("getServicesList", "{url}/service", "get", removeDuplicates),
        ("getService", "{url}/service/{servicename}"),
        ("getServiceForUser", "{url}/user/{userId}/service/{servicename}"),
        ("removeServiceForUser",
         "{url}/user/{userId}/service/{servicename}", "delete", refreshUserServices)
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
        ("createResearch", "{url}/user/{userId}", "post", refreshProjects),
        ("saveResearch",
         "{url}/user/{userId}/research/{researchId}", "post", refreshProjects),
        ("removeAllResearch", "{url}/user/{userId}",
         "delete", refreshProjects),
        ("removeResearch",
         "{url}/user/{userId}/research/{researchId}", "delete", refreshProjects),
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


def exchangeCodeData(data):
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


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        LOGGER.info("logged? {}, {}, {}".format(
            current_user.is_authenticated, args, kwargs))

        emit("LoginStatus", json.dumps({
            "status": current_user.is_authenticated,
            "user": current_user.userId
        }))

        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.event("triggerSynchronization")
@authenticated_only
def triggerSynchronization(json):
    httpManager.makeRequest("triggerFileSynchronization", data=json)
    httpManager.makeRequest("triggerMetadataSynchronization", data=json)
    httpManager.makeRequest("finishResearch", data=json)


@socketio.on("connect")
@authenticated_only
def connected():
    current_user.websocketId = request.sid
    clients[current_user.userId] = current_user

    emit("ServiceList", httpManager.makeRequest("getServicesList"))
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))
    emit("ProjectList", httpManager.makeRequest("getAllResearch"))


@socketio.on("disconnect")
def disconnect():
    LOGGER.info("disconnected")

    try:
        LOGGER.debug("LOGOUT")
        # logout_user()
        #del clients[current_user.userId]
    except Exception as e:
        LOGGER.error(e, exc_info=True)


@socketio.on("sendMessage")
@authenticated_only
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

    req = exchangeCodeData(jsonData)
    LOGGER.debug(req.text)

    # update userserviceslist on client
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))

    return req.status_code < 300


@socketio.event
@authenticated_only
def changePorts(jsonData):
    """
    return {
        researchID: researchID,
        import: {
            add: [{name: "port-owncloud", filepath:"/photosForschung/"}],
        },
        export: {
            add: [{name: "port-zenodo"} ],
            remove: ["port-reva", "port-osf"],
            change: [{name: "port-owncloud", filepath:"/photosForschung/"}, {name: "port-zenodo", projectId:"12345"}]
        }
    }"""
    jsonData = json.loads(jsonData)
    researchId = jsonData["researchID"]

    user = current_user.userId
    urlResearch = os.getenv(
        "CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

    def transformPorts(type, portList):
        data = []
        for port in portList[type]:
            obj = {
                "port": port["name"],
                "properties": [
                    {
                        "portType": "filestorage",
                        "value": "True"
                    }
                ]
            }
            if "filepath" in port:
                obj["properties"].append({
                    "portType": "customProperties",
                    "value": {
                        "key": "filepath",
                        "value": port["filepath"]
                    }
                })
            if "projectId" in port:
                obj["properties"].append({
                    "portType": "customProperties",
                    "value": {
                        "key": "projectId",
                        "value": port["projectId"]
                    }
                })
            data.append(obj)
        return data

    for method in ["add", "change"]:
        requests.post(f"{urlResearch}/user/{user}/research/{researchId}/imports",
                      json=transformPorts(method, jsonData["import"]))
        requests.post(f"{urlResearch}/user/{user}/research/{researchId}/exports",
                      json=transformPorts(method, jsonData["export"]))

    def getIdPortListForRemoval(portList):
        """Get Id Port list
        Works only with remove command.
        """
        portList = []
        for portType in ["imports", "exports"]:
            ports = requests.get(
                f"{urlResearch}/user/{user}/research/{researchId}/{portType}").json
            for port in ports:
                for givenPort in portList:
                    if port.port == givenPort:
                        portList.append((portType, port.id))
                        break
        return portList

    for t in ["import", "export"]:
        for portType, portId in getIdPortListForRemoval(jsonData[t]["remove"]):
            requests.delete(
                f"{urlResearch}/user/{user}/research/{researchId}/{portType}/{portId}")

    return jsonData
