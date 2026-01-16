from dataclasses import dataclass, field
import lxml
from xsdata.formats.dataclass.parsers import XmlParser
import xml.etree.ElementTree as ET

from .dapi_error_handler import DapiErrorHandler
from ...onix.onix_book_product_3_1_reference import Onixmessage

@dataclass
class GetRecordsX(DapiErrorHandler):
    namespaces = {
        'dilve': 'http://www.dilve.es/dilve/api/xsd/getRecordsXResponse',
        'onix': 'http://ns.editeur.org/onix/3.1/reference'
    }

    onixMessage: Onixmessage

    def __init__(self, response):
        tree = lxml.etree.XML(response.encode('utf-8'))
        self._DapiErrorHandler__parse_error(tree.find("dilve:error", self.namespaces))

        self.onixMessage = XmlParser().parse(tree.find('onix:ONIXMessage', self.namespaces), Onixmessage)