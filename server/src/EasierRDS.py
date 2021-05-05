import logging
import requests
import os
import json
from flask_login import current_user
from .app import use_predefined_user

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def parseDict(data, socketio=None, httpManager=None):
    if (socketio or httpManager) is None:
        raise ValueError("socketio and httpManager are none.")

    httpManager = httpManager or HTTPManager(socketio=socketio)

    for key, value in data.items():
        http = HTTPRequest(key)

        for val in value:
            http.addRequest(*val)

        httpManager.addService(http)

    return httpManager


class HTTPRequest:
    def __init__(self, url):
        self.url = url
        self.requestList = {}

    def addRequest(self, key, url, method="get", function=None, afterFunction=None):
        self.requestList[key] = {
            "url": url,
            "method": method,
            "function": function
        }

    def makeRequest(self, key, data=None):
        if data is None:
            data = {}

        if isinstance(data, str):
            data = json.loads(data)

        reqConf = self.requestList[key]

        if reqConf["method"].lower() != "get" and reqConf["function"] is not None and not reqConf["function"].__name__.startswith("refresh"):
            try:
                data = reqConf["function"](data)
            except:
                pass

        if use_predefined_user:
            data["userId"] = os.getenv("DEV_FLASK_USERID")
        else:
            data["userId"] = current_user.userId

        data["url"] = self.url

        LOGGER.debug("key: {}, data: {}, req: {}".format(key, data, reqConf))

        url = reqConf["url"].format(**data)
        LOGGER.debug("request url: {}".format(url))
        req = getattr(requests, reqConf["method"])(
            url, json=data, verify=os.getenv("VERIFY_SSL", "False") == "True"
        )

        LOGGER.debug(
            "status_code: {}, content: {}".format(req.status_code, req.text))

        response = req.text
        if reqConf["method"].lower() == "get":
            try:
                response = json.dumps(
                    reqConf["function"](json.loads(req.text)))
            except:
                pass

        if reqConf["function"] is not None and reqConf["function"].__name__.startswith("refresh"):
            reqConf["function"]()

        return response


class HTTPManager:
    def __init__(self, socketio):
        self.services = []
        self.socketio = socketio

    def addService(self, service: HTTPRequest):
        if not isinstance(service, HTTPRequest):
            raise ValueError

        self.services.append(service)

        for key in service.requestList.keys():
            def outerFn(key):
                def reqFn(*args):
                    try:
                        return service.makeRequest(key, *args)
                    except Exception as e:
                        LOGGER.error(
                            "make request error: {}".format(e), exc_info=True)
                return reqFn

            self.socketio.on_event(key, outerFn(key))

    def makeRequest(self, *args, **kwargs):
        for service in self.services:
            try:
                return service.makeRequest(*args, **kwargs)
            except Exception as e:
                LOGGER.error("make request error: {}".format(e), exc_info=True)

        raise ValueError("no service implements the given url.")
