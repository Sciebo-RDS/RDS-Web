import logging
import requests
import os
from flask_login import current_user

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


class HTTPRequest:
    def __init__(self, url):
        self.url = url
        self.requestList = {}

    def addRequest(self, key, url, method="get", function=None):
        self.requestList[key] = {
            "url": url,
            "method": method,
            "function": function
        }

    def makeRequest(self, key, data=None):
        if data is None or not isinstance(data, dict):
            data = {}

        try:
            data["userId"] = current_user.userId
        except:
            data["userId"] = "admin"

        data["url"] = self.url
        reqConf = self.requestList[key]

        LOGGER.debug("key: {}, data: {}, req: {}".format(key, data, reqConf))

        url = reqConf["url"].format(**data)
        LOGGER.debug("request url: {}".format(url))
        req = getattr(requests, reqConf["method"])(
            url, json=data, verify=False)

        LOGGER.debug(
            "status_code: {}, content: {}".format(req.status_code, req.text))

        if reqConf["function"] is not None:
            return reqConf["function"](req.text)
        return req.text


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
                        return service.makeRequest(key, args)
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
