import os
import requests
from flask import session
import logging

LOGGER = logging.getLogger()


def getSessionId(access_token=None, folder=None):
    informations = session["informations"]

    if access_token is not None:
        informations["access_token"] = access_token

    if folder is not None and isinstance(folder, str):
        informations["folder"] = folder

    informations["url"] = "{}/remote.php/dav".format(
        os.getenv("OWNCLOUD_URL", "http://localhost:8000")
    )

    payload = {
        "email": informations["email"],
        "name": informations["name"],
        "session": {
            "owncloud": informations
        }
    }

    headers = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer {}".format(os.getenv("DESCRIBO_API_SECRET"))
    }

    LOGGER.debug("send payload: {}".format(payload))

    req = requests.post(
        os.getenv("DESCRIBO_API_ENDPOINT"),
        json=payload,
        headers=headers
    )

    return req.json().get("sessionId")
