import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET
from .dapi_error_handler import DapiErrorHandler

_logger = logging.getLogger(__name__)

@dataclass
class GetRecordStatusX(DapiErrorHandler):
    namespaces = {'dilve': 'http://www.dilve.es/dilve/api/xsd/getRecordStatusXResponse'}

    @dataclass
    class Header:
        fromDate: datetime
        toDate: datetime

    @dataclass
    class Record:
        id: "RecordID"

    @dataclass
    class RecordID:
        type: str
        value: str

    header: Header
    existingRecords: int
    newRecords: List[Record]
    changedRecords: List[Record]
    deletedRecords: List[Record]

    def __init__(self, response):
        root = ET.fromstring(response)

        self._DapiErrorHandler__parse_error(root.find("dilve:error", self.namespaces))

        self.header = self.__parse_header(root.find("dilve:header", self.namespaces))
        self.existingRecords = self.__parse_existing_records(root.find("dilve:existingRecords", self.namespaces))
        self.newRecords = self.__parse_records(root.find("dilve:newRecords", self.namespaces))
        self.changedRecords = self.__parse_records(root.find("dilve:changedRecords", self.namespaces))
        self.deletedRecords = self.__parse_records(root.find("dilve:deletedRecords", self.namespaces))

    def __parse_header(self, header):
        from_date_str = header.find("dilve:fromDate", self.namespaces)
        to_date_str = header.find("dilve:toDate", self.namespaces)
        from_date = datetime.strptime(from_date_str.text, '%Y-%m-%dT%H:%M:%SZ')
        to_date = datetime.strptime(to_date_str.text, '%Y-%m-%dT%H:%M:%SZ')
        return GetRecordStatusX.Header(fromDate=from_date, toDate=to_date)

    def __parse_existing_records(self, existingRecords):
        return existingRecords.attrib.get("count")

    def __parse_records(self, xml_records):
        records = xml_records.findall("dilve:record", self.namespaces)
        return [self.__parse_record(record) for record in records]

    def __parse_record(self, xml_record):
        record = xml_record.find("dilve:id", self.namespaces)
        record_id = GetRecordStatusX.RecordID(type=record.attrib.get("type"), value=record.text)
        return GetRecordStatusX.Record(id=record_id)
