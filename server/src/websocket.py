from flask import Blueprint, request, redirect, render_template
from flask_socketio import send, emit, disconnect, join_room, leave_room
from flask_login import current_user, logout_user
from .Util import parseResearch, parseAllResearch, parseResearchBack, parseAllResearchBack, parsePortBack, removeDuplicates
from .EasierRDS import parseDict
from .app import socketio, clients
from .Describo import getSessionId
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


url = os.getenv("RDS_INSTALLATION_DOMAIN")

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
        ("getAllFiles", "{url}/user/{userId}/research/{researchIndex}"),
        ("triggerFileSynchronization",
         "{url}/user/{userId}/research/{researchIndex}", "post"),
        ("removeAllFiles",
         "{url}/user/{userId}/research/{researchIndex}", "delete")
    ],
    os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"): [
        ("getAllResearch", "{url}/user/{userId}", "get", parseAllResearch),
        ("getResearch",
         "{url}/user/{userId}/research/{researchIndex}", "get", parseResearch),
        ("createResearch", "{url}/user/{userId}", "post", refreshProjects),
        ("saveResearch",
         "{url}/user/{userId}/research/{researchIndex}", "post", refreshProjects),
        ("removeAllResearch", "{url}/user/{userId}",
         "delete", refreshProjects),
        ("removeResearch",
         "{url}/user/{userId}/research/{researchIndex}", "delete", refreshProjects),
        ("addImport",
         "{url}/user/{userId}/research/{researchIndex}/imports", "post", parsePortBack),
        ("addExport",
         "{url}/user/{userId}/research/{researchIndex}/exports", "post", parsePortBack),
        ("removeImport",
         "{url}/user/{userId}/research/{researchIndex}/imports/{portId}", "delete"),
        ("removeExport",
         "{url}/user/{userId}/research/{researchIndex}/exports/{portId}", "delete")
    ],
    os.getenv("USE_CASE_SERVICE_METADATA_SERVICE", f"{url}/metadata"): [
        ("finishResearch",
         "{url}/user/{userId}/research/{researchIndex}", "put"),
        ("triggerMetadataSynchronization",
         "{url}/user/{userId}/research/{researchIndex}", "patch")
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
    requestSessionId()


@socketio.on("disconnect")
def disconnect():
    LOGGER.info("disconnected")

    try:
        LOGGER.debug("LOGOUT")
        # logout_user()
        # del clients[current_user.userId]
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
        researchIndex: researchIndex,
        import: {
            add: [{name: "port-owncloud", filepath:"/photosForschung/"}],
        },
        export: {
            add: [{name: "port-zenodo"} ],
            remove: ["port-reva", "port-osf"],
            change: [{name: "port-owncloud", filepath:"/photosForschung/"},
                {name: "port-zenodo", projectId:"12345"}]
        }
    }"""
    if jsonData is None:
        return

    jsonData = json.loads(jsonData)
    researchIndex = jsonData["researchIndex"]

    user = current_user.userId
    urlResearch = os.getenv(
        "CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

    def transformPorts(portList):
        data = []
        for port in portList:
            obj = {
                "port": port["servicename"],
                "properties": []
            }

            if "filepath" in port:
                obj["properties"].append(
                    {
                        "portType": "fileStorage",
                        "value": True
                    }
                )
                obj["properties"].append({
                    "portType": "customProperties",
                    "value": [{
                        "key": "filepath",
                        "value": port["filepath"]
                    }]
                })
            else:
                obj["properties"].append(
                    {
                        "portType": "metadata",
                        "value": True
                    }
                )

            if "projectId" in port:
                obj["properties"].append({
                    "portType": "customProperties",
                    "value": [{
                        "key": "projectId",
                        "value": port["projectId"]
                    }]
                })
            data.append(obj)
        LOGGER.debug(f"transform data: {data}")
        return data

    crossPort = {
        "import": "imports",
        "export": "exports"
    }

    for portOutLight, portOutRight in crossPort.items():
        for method in ["add", "change"]:
            for port in transformPorts(jsonData[portOutLight][method]):
                requests.post(
                    f"{urlResearch}/user/{user}/research/{researchIndex}/{portOutRight}",
                    json=port,
                    verify=os.getenv("VERIFY_SSL", "False") == "True"
                )

    def getIdPortListForRemoval(portList):
        """Get Id Port list
        Works only with remove command.
        """
        retPortList = []
        for portType in crossPort.values():
            ports = requests.get(
                f"{urlResearch}/user/{user}/research/{researchIndex}/{portType}",
                verify=os.getenv("VERIFY_SSL", "False") == "True").json()
            for index, port in enumerate(ports):
                for givenPort in portList:
                    if port["port"] == givenPort["servicename"]:
                        retPortList.append((portType, index))
                        break
        return retPortList

    for t in crossPort.keys():
        for portType, portId in getIdPortListForRemoval(jsonData[t]["remove"]):
            LOGGER.debug(f"type: {portType}, id: {portId}")
            requests.delete(
                f"{urlResearch}/user/{user}/research/{researchIndex}/{portType}/{portId}",
                verify=os.getenv("VERIFY_SSL", "False") == "True")

    emit("ProjectList", httpManager.makeRequest("getAllResearch"))


@socketio.event
def requestSessionId():
    try:
        token = json.loads(httpManager.makeRequest(
            "getServiceForUser", {
                "servicename": "port-owncloud"
            }
        ))["data"]["access_token"]
        emit("SessionId", getSessionId(token))
    except:
        pass
