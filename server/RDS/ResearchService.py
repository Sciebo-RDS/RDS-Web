import os
import requests
import logging

url = os.getenv("CIRCLE3_RESEARCH_MANAGER",
                "http://circle3-research-manager/research")

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def getResearchList(user_id):
    data = requests.get("{}/user/{}".format(url, user_id))
    LOGGER.debug("user {}, get research, status_code: {}".format(
        user_id, data.status_code))
    return data.content


def removeResearch(user_id, research_id):
    data = requests.delete(
        "{}/user/{}/research/{}".format(url, user_id, research_id))
    LOGGER.debug("user {}, remove research {}, status_code: {}".format(
        user_id, research_id, data.status_code))
    return data.content


def createResearch(user_id):
    data = requests.post(
        "{}/user/{}".format(url, user_id))
    LOGGER.debug("user {}, create research, status_code: {}".format(
        user_id, data.status_code))
    return data.content


def getResearch(user_id, research_id):
    data = requests.get("{}/user/{}/research".format(url, user_id))
    LOGGER.debug("user {}, get research {}, status_code: {}".format(
        user_id, research_id, data.status_code))
    return data.content


def addImport(user_id, research_id, port):
    data = requests.post(
        "{}/user/{}/research/{}/imports".format(url, user_id, research_id), json=port)

    LOGGER.debug("user {}, add import {} to research {}, status_code: {}".format(
        user_id, port, research_id, data.status_code))

    return data.content


def removeImport(user_id, research_id, port):
    data = requests.delete(
        "{}/user/{}/research/{}/imports/{}".format(url, user_id, research_id, port.id))
    LOGGER.debug("user {}, remove import {} to research {}, status_code: {}".format(
        user_id, port, research_id, data.status_code))
    return data.content


def addExport(user_id, research_id, port):
    data = requests.post(
        "{}/user/{}/research/{}/exports".format(url, user_id, research_id), json=port.toJson())
    LOGGER.debug("user {}, add export {} to research {}, status_code: {}".format(
        user_id, port, research_id, data.status_code))
    return data.content


def removeExport(user_id, research_id, port):
    data = requests.delete(
        "{}/user/{}/research/{}/exports/{}".format(url, user_id, research_id, port.id))
    LOGGER.debug("user {}, remove export {} to research {}, status_code: {}".format(
        user_id, port, research_id, data.status_code))
    return data.content


def pushStatus(user_id, research_id):
    data = requests.patch(
        "{}/user/{}/research/{}/status".format(url, user_id, research_id))
    LOGGER.debug("patch status for researchid {}, status_code: {}".format(
        research_id, data.status_code))
    return data.content
