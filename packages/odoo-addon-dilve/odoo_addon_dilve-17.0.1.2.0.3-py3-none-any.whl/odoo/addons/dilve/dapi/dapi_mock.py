import os
import logging
from datetime import datetime

from .data_classes import GetRecordsX, GetResourceX, GetRecordStatusX, GetRecordListX


_logger = logging.getLogger(__name__)

class DapiClient:

    def __init__(self, user="", pswd=""):
        self.user = user
        self.pswd = pswd

    def getRecordsX(self, identifier, version="3.1"):
        current_dir = os.path.dirname(__file__)
        module_root = os.path.dirname(current_dir)
        file_path = os.path.join(module_root, "sample_data", f"{identifier}.xml")
        if not os.path.isfile(file_path):
            file_path = os.path.join(module_root, "sample_data", "978-84-121353-3-6.xml")

        with open(file_path, "r") as sample_dilve_response:
            response = sample_dilve_response.read()

        return GetRecordsX(response)

    async def getRecordsX_async(self, identifier, version="3.1"):
        return self.getRecordsX(identifier)

    def getResourceX(self, identifier, resource_id):
        current_dir = os.path.dirname(__file__)
        module_root = os.path.dirname(current_dir)
        file_path = os.path.join(module_root, "sample_data", f"{identifier}.jpg")
        if not os.path.isfile(file_path):
            file_path = os.path.join(module_root, "sample_data", "9788412135336.jpg")


        with open(file_path, "rb") as sample_dilve_response:
            response = sample_dilve_response.read()

        return GetResourceX(response)

    def getRecordStatusX(self, publisher_code, from_date, to_date=datetime.today()):
        current_dir = os.path.dirname(__file__)
        module_root = os.path.dirname(current_dir)
        file_path = os.path.join(module_root, "sample_data", "getRecordStatusXResponse.xml")

        with open(file_path, "r") as sample_dilve_response:
            response = sample_dilve_response.read()

        return GetRecordStatusX(response)

    def getRecordListX(self, publisher_code):
        current_dir = os.path.dirname(__file__)
        module_root = os.path.dirname(current_dir)
        file_path = os.path.join(module_root, "sample_data", "getRecordListXResponse.xml")

        with open(file_path, "r") as sample_dilve_response:
            response = sample_dilve_response.read()

        return GetRecordListX(response)