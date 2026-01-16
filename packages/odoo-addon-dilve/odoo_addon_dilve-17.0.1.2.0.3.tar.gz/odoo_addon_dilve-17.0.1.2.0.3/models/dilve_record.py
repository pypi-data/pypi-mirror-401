import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class DilveRecord(models.TransientModel):
    _name = "dilve.record"
    _description = "Dilve record"

    is_selected = fields.Boolean(required=False)
    isbn = fields.Char(string='Isbn')
    name = fields.Char(string='Nombre', required=False)
    type = fields.Selection(
        string='Type',
        selection=[('new', 'Nuevo'),
                   ('changed', 'Moficado'),
                   ("existing", "Existente")],
        required=False
    )
