import os
import logging
from enum import Enum
import requests
from datetime import datetime

from .data_classes import GetRecordsX, GetResourceX, GetRecordStatusX, GetRecordListX

_logger = logging.getLogger(__name__)

class DapiEndpoints(Enum):
    GET_RECORDS_X = "getRecordsX.do"
    GET_RESOURCE_X = "getResourceX.do"
    GET_RECORD_STATUS_X = "getRecordStatusX.do"
    GET_RECORD_LIST_X = "getRecordListX.do"

class DapiClient:

    URL = "https://www.dilve.es/dilve/dilve/"

    def __init__(self, session, user, pswd):
        self.session = session
        self.user = user
        self.pswd = pswd

    def getRecordsX(self, identifier, version="3.1"):
        _logger.info("API Request: getRecordsX")
        args = {
            "identifier": identifier,
            "version": version
        }

        response = self.__get(DapiEndpoints.GET_RECORDS_X.value, args)
        return GetRecordsX(response)

    async def getRecordsX_async(self, identifier, version="3.1"):
        _logger.info("API Request: getRecordsX")
        args = {
            "identifier": identifier,
            "version": version
        }

        response = await self.__async_get(DapiEndpoints.GET_RECORDS_X.value, args)
        return GetRecordsX(response)

    def getResourceX(self, identifier, resource_id):
        _logger.info("API Request: getResourceX")
        args = {
            "identifier": identifier,
            "resource": resource_id
        }

        response = self.__get(DapiEndpoints.GET_RESOURCE_X.value, args)
        return GetResourceX(response)

    def getRecordStatusX(self, publisher_code, from_date, to_date=datetime.today()):
        _logger.info("API Request: getRecordStatusX")
        args = {
            "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "publisher": publisher_code,
            "hyphens": "Y"
        }

        response = self.__get(DapiEndpoints.GET_RECORD_STATUS_X.value, args)
        return GetRecordStatusX(response)

    def getRecordListX(self, publisher_code):
        _logger.info("API Request: getRecordListX")
        args = {
            "publisher": publisher_code,
            "hyphens": "Y"
        }

        response = self.__get(DapiEndpoints.GET_RECORD_LIST_X.value, args)
        return GetRecordListX(response)


    async def __async_get(self, endpoint: str, args: dict = None):
        try:
            url = self.URL + endpoint

            params = {
                "user": self.user,
                "password": self.pswd,
                **args
            }
            async with self.session.get(url=url, params=params) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type")
                    if content_type.startswith("image"):
                        data = await response.read()
                    else:
                        data = await response.text()

                    return data
                else:
                    _logger.error(f"Response Code: {response.status_code}")
                    return None
        except requests.exceptions.RequestException as e:
            _logger.error(e)
        except Exception as e:
            _logger.error(e)

    def __get(self, endpoint: str, args: dict = None):
        try:
            url = self.URL + endpoint
            params = {
                "user": self.user,
                "password": self.pswd,
                **args
            }
            response = requests.get(url=url, params=params)
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type")
                if content_type.startswith("image"):
                    data = response.content
                else:
                    data = response.text

                return data
            else:
                _logger.error(f"Response Code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            _logger.error(e)
        except Exception as e:
            _logger.error(e)
