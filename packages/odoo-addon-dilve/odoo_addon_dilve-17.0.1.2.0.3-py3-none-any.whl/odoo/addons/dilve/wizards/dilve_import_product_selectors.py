from odoo import fields, models, api

class DilveImportProductSelectors(models.AbstractModel):
    _name = "dilve.import.product.selectors"
    select_all_fields = fields.Boolean(string="Seleccionar todos los campos", default=False, required=False)
    product_name_selector = fields.Boolean(string="Título", help="Override product name?", default=False, required=False)
    product_cover_selector = fields.Boolean(string="Portada", help="Override product cover?", default=False, required=False)
    tags_selector = fields.Boolean(string="Etiquetas", help="Override product tags?", default=False, required=False)
    pvp_selector = fields.Boolean(string="PVP", help="Override product RRP?", default=False, required=False)
    category_selector = fields.Boolean(string="Category", help="Override product category?", default=False, required=False)
    collections_selector = fields.Boolean(string="Colecciones", help="Override product collections?", default=False, required=False)
    taxes_selector = fields.Boolean(string="Impuestos cliente", help="Override product taxes?", default=False, required=False)
    weight_selector = fields.Boolean(string="Peso", help="Override product weight?", default=False, required=False)
    length_selector = fields.Boolean(string="Largo", help="Override product length?", default=False, required=False)
    width_selector = fields.Boolean(string="Ancho", help="Override product width?", default=False, required=False)
    height_selector = fields.Boolean(string="Alto", help="Override product height?", default=False, required=False)
    authorship_selector = fields.Boolean(string="Autoras", help="Override product authorship?", default=False, required=False)
    page_count_selector = fields.Boolean(string="Páginas", help="Override product page count?", default=False, required=False)
    total_copies_selector = fields.Boolean(string="Ejemplares impresos", help="Override product total copies?", default=False, required=False)

    @api.onchange('select_all_fields')
    def _onchange_select_all_fields_base(self):
        value = self.select_all_fields
        for field in self.fields_get():
            if "_selector" in field:
                self[field] = value


