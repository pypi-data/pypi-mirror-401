import logging
from odoo import fields, models, api

from .dilve_base import DilveBase
from .dilve_import_product_selectors import DilveImportProductSelectors

_logger = logging.getLogger(__name__)

class DilveImportProductWizard(models.TransientModel, DilveImportProductSelectors, DilveBase):
    _name = "dilve.import.product.wizard"
    _description = "Import Product from DILVE"

    product = fields.Many2one(comodel_name="product.template", string="Product", required=True)

    product_cover = fields.Binary(string="Portada")
    product_name = fields.Char(string="Título")
    authorship = fields.Many2many(comodel_name="authorship.product", string="Autoras")
    tags = fields.Many2many(comodel_name="product.tag", string="Etiquetas")
    pvp = fields.Float(string="PVP")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Moneda", default=lambda self: self.env.company.currency_id)
    category = fields.Many2one(comodel_name="product.category", string="Category")
    collections = fields.Many2many(comodel_name="product.template.collection", string="Colecciones")
    taxes = fields.Many2many(comodel_name="account.tax", string="Impuestos cliente")
    type = fields.Char(string="Type")
    weight = fields.Float(string="Peso")
    weight_uom_id = fields.Many2one(comodel_name="uom.uom", string="Weight Unit of Measure")
    length = fields.Float(string="Largo")
    width = fields.Float(string="Ancho")
    height = fields.Float(string="Alto")
    dimensional_uom_id = fields.Many2one(comodel_name="uom.uom", string="Dimension Unit of Measure")
    page_count = fields.Integer(string="Páginas")
    total_copies = fields.Integer(string="Ejemplares impresos")

    @api.onchange('product')
    def get_product_from_dilve(self):
        _logger.info("get_product_from_dilve")
        isbn = self.product.isbn_number
        data = self.get_api().getRecordsX(identifier=isbn)
        values = self.map_product(data.onixMessage)
        self.map_dilve(values)

    def map_dilve(self, dict):
        self.product_name = dict.get("product_name")
        self.authorship = dict.get("authorship")
        self.tags = dict.get("tags")
        self.product_cover = dict.get("product_cover")
        self.pvp = dict.get("pvp")
        self.category = dict.get("category")
        self.collections = dict.get("collections")
        self.taxes = dict.get("taxes")
        self.type = dict.get("type")
        self.weight = dict.get("weight")
        self.weight_uom_id = dict.get("weight_uom_id")
        self.length = dict.get("length")
        self.width = dict.get("width")
        self.height = dict.get("height")
        self.dimensional_uom_id = dict.get("dimensional_uom_id")
        self.page_count = dict.get("page_count")
        self.total_copies = dict.get("total_copies")

    def import_product(self):
        _logger.info(f"Updating book [{self.product_name}]...")
        try:
            data = {"type": self.type}

            if self.product_name_selector: data["name"] = self.product_name
            if self.authorship_selector: data["authorship_ids"] = self.authorship
            if self.product_cover_selector: data["image_1920"] = self.product_cover
            if self.tags_selector: data["product_tag_ids"] = self.tags
            if self.pvp_selector: data["list_price"] = self.pvp
            if self.category_selector: data["categ_id"] = self.category
            if self.collections_selector: data["collections"] = self.collections
            if self.taxes_selector: data["taxes_id"] = self.taxes
            if self.weight_selector:
                data["product_weight"] = self.weight
                data["weight_uom_id"] = self.weight_uom_id
            if self.length_selector:
                data["product_length"] = self.length
                data["dimensional_uom_id"] = self.dimensional_uom_id
            if self.width_selector:
                data["product_width"] = self.width
                data["dimensional_uom_id"] = self.dimensional_uom_id
            if self.height_selector:
                data["product_height"] = self.height
                data["dimensional_uom_id"] = self.dimensional_uom_id
            if self.page_count_selector:
                data["page_count"] = self.page_count
            if self.total_copies_selector:
                data["total_copies"] = self.total_copies

            self.product.write(data)

            _logger.info(f"Book [{self.product_name}] imported successfully.")
        except Exception as e:
            _logger.error(f"Exception importing book [{self.product_name}]:", exc_info=e)

        return {'type': 'ir.actions.act_window_close'}
