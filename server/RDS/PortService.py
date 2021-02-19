import requests
import os
import logging

url = os.getenv("CIRCLE2_PORT_SERVICE",
                "http://circle2-port-service/port-service")
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def getServicesList():
    req = requests.get("{}/service".format(url))
    LOGGER.debug("get servicelist, status_code: {}".format(
        req.status_code))
    return req.content


def getService(service):
    req = requests.get("{}/service/{}".format(url, service))
    LOGGER.debug("get service {}, status_code: {}".format(
        service, req.status_code))
    return req.content


def getUserServices(user_id):
    req = requests.get("{}/user/{}/service".format(url, user_id))
    LOGGER.debug("user {}, get user services, status_code: {}".format(
        user_id, req.status_code))
    return req.content


def getServiceForUser(user_id, service):
    req = requests.get(
        "{}/user/{}/service/{}".format(url, user_id, service))
    LOGGER.debug("user {}, get service {}, status_code: {}".format(
        user_id, service, req.status_code))
    return req.content


def removeServiceForUser(user_id, service):
    req = requests.delete(
        "{}/user/{}/service/{}".format(url, user_id, service))
    LOGGER.debug("user {}, remove service {}, status_code: {}".format(
        user_id, service, req.status_code))
    return req.content
