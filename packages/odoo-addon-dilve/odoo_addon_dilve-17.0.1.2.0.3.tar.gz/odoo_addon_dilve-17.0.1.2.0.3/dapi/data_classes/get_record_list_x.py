import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET
from .dapi_error_handler import DapiErrorHandler

_logger = logging.getLogger(__name__)

@dataclass
class GetRecordListX(DapiErrorHandler):
    namespaces = {'dilve': 'http://www.dilve.es/dilve/api/xsd/getRecordListXResponse'}

    @dataclass
    class Header:
        listDate: datetime

    @dataclass
    class Record:
        id: "RecordID"

    @dataclass
    class RecordID:
        type: str
        value: str

    header: Header
    totalRecords: int
    records: List[Record]

    def __init__(self, response):
        root = ET.fromstring(response)

        self._DapiErrorHandler__parse_error(root.find("dilve:error", self.namespaces))

        self.header = self.__parse_header(root.find("dilve:header", self.namespaces))
        self.totalRecords = self.__parse_total_records(root.find("dilve:totalRecords", self.namespaces))
        self.records = self.__parse_records(root.find("dilve:records", self.namespaces))

    def __parse_header(self, header):
        list_date_str = header.find("dilve:listDate", self.namespaces)
        list_date = datetime.strptime(list_date_str.text, '%Y-%m-%dT%H:%M:%SZ')
        return GetRecordListX.Header(listDate=list_date)

    def __parse_total_records(self, totalRecords):
        return totalRecords.attrib.get("count")

    def __parse_records(self, xml_records):
        records = xml_records.findall("dilve:record", self.namespaces)
        return [self.__parse_record(record) for record in records]

    def __parse_record(self, xml_record):
        record = xml_record.find("dilve:id", self.namespaces)
        record_id = GetRecordListX.RecordID(type=record.attrib.get("type"), value=record.text)
        return GetRecordListX.Record(id=record_id)
