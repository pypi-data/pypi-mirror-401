from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    _check_company_auto = True

    dilve_user = fields.Char(string="Dilve Username", help="DILVE username")
    dilve_pass = fields.Char(string="Dilve Password", help="DILVE password")
    dilve_publisher_code = fields.Char(string="Dilve Publisher Code", help="DILVE publisher code")
    dilve_last_checked = fields.Datetime(string='DILVE last checked', required=False)
