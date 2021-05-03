import os
import requests
from flask import session
import logging

LOGGER = logging.getLogger()


def getSessionId(access_token):
    informations = session["informations"]

    if not informations["access_token"]:
        informations["access_token"] = access_token

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

    req = requests.post(
        os.getenv("DESCRIBO_API_ENDPOINT"),
        json=payload,
        headers=headers
    )

    return req.json().get("sessionId")
