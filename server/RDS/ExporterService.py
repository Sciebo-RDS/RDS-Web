import requests
import os
import logging

url = os.getenv("CIRCLE2_EXPORTER_SERVICE",
                "http://circle2-exporter-service/exporter")
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def getAllFiles(user_id, research_id):
    pass


def removeFilesInExport(user_id, research_id):
    pass


def triggerFileSync(user_id, research_id):
    pass


def getFilesFromService(user_id, research_id, service):
    pass


def triggerFileSyncForService(user_id, research_id, service):
    pass


def removeFilesInExportFromService(user_id, research_id, service):
    pass


def getFileFromService(user_id, research_id, service, file_id):
    pass


def triggerFileSyncForServiceFile(user_id, research_id, service, file_id):
    pass


def removeFileInExportFromServiceFile(user_id, research_id, service, file_id):
    pass
