import os
import requests
import logging

url = os.getenv("CIRCLE2_METADATA_SERVICE",
                "http://circle2-metadata-service/metadata")

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def finishResearch(user_id, research_id):
    req = requests.put("{}/user/{}/research/{}".format(url, research_id))
    LOGGER.debug("user {}, finish research {}, status_code: {}".format(
        user_id, research_id, req.status_code))
    return req.content


def triggerMetadata(user_id, research_id):
    req = requests.patch("{}/user/{}/research/{}".format(url, research_id))
    LOGGER.debug("user {}, trigger metadata for research {}, status_code: {}".format(
        user_id, research_id, req.status_code))
    return req.content
