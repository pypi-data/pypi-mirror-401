from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    dilve_user = fields.Char(string="Dilve username", related="company_id.dilve_user", help="DILVE username", readonly=False)
    dilve_pass = fields.Char(string="Dilve Password", related="company_id.dilve_pass", help="DILVE password", readonly=False)

    dilve_publisher_code = fields.Char(string="Dilve publisher code", related="company_id.dilve_publisher_code", help="DILVE publisher code", readonly=False)

    def write(self, values):
        res = super(ResConfigSettings, self).write(values)

        if "dilve_user" in values:
            self.env.company.write({"dilve_user": values.get("dilve_user")})

        if "dilve_pass" in values:
            self.env.company.write({"dilve_pass": values.get("dilve_pass")})

        if "dilve_publisher_code" in values:
            self.env.company.write({"dilve_publisher_code": values.get("dilve_publisher_code")})

        return res