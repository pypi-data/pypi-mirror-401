import os
import json
import logging
from pathlib import Path

_logger = logging.getLogger(__name__)

class Thema:

    def __init__(self):
        try:
            file_path = Path(__file__).with_name("20250204_Thema_v1.6_es.json")
            with file_path.open("r") as file:
                data = json.load(file)
                self.codes = data["CodeList"]["ThemaCodes"]["Code"]
        except json.JSONDecodeError as e:
            _logger.error(f"JSONDecodeError: {e}")

    def get_from_code(self, code_value):
        for code in self.codes:
            if code["CodeValue"] == code_value:
                return code["CodeDescription"]