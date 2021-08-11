import os
import requests
from flask import session
import logging

LOGGER = logging.getLogger()


def getSessionId(access_token=None, folder=None):
    informations = session["informations"]
    data = {
        "user_id": informations["UID"],
        "url": "{}/remote.php/dav".format(
            os.getenv("OWNCLOUD_URL", "http://localhost:8000")
        ),
    }

    if access_token is not None:
        data["access_token"] = access_token

    if folder is not None and isinstance(folder, str):
        data["folder"] = folder

    payload = {
        "email": informations["email"],
        "name": informations["name"],
        "session": {
            "owncloud": data
        }
    }

    headers = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer {}".format(os.getenv("DESCRIBO_API_SECRET"))
    }

    LOGGER.debug("send payload: {}, headers: {}".format(payload, headers))

    req = requests.post(
        os.getenv("DESCRIBO_API_ENDPOINT"),
        json=payload,
        headers=headers
    )

    LOGGER.debug("response:\nheaders: {}\nbody: {}".format(
        req.headers, req.text))

    return req.json().get("sessionId")
