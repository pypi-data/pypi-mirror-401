import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DapiErrorHandler:

    def __parse_error(self, error):
        if error:
            code = error.find("dilve:code", self.namespaces).text
            text = error.find("dilve:text", self.namespaces).text
            _logger.error("Dilve Error:")
            _logger.error(f"    Code: {code}")
            _logger.error(f"    Text: {text}")
            raise UserError(f"DILVE error ({code}) - {text}")