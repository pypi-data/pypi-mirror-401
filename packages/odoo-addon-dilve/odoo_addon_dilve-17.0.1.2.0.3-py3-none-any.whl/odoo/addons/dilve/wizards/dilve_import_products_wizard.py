import logging
import io
from odoo import fields, models, api
from datetime import datetime
import traceback
import base64
import time
import asyncio
import aiohttp

from .dilve_base import DilveBase
from .dilve_import_product_selectors import DilveImportProductSelectors

_logger = logging.getLogger(__name__)

class DilveImportProductsWizard(DilveImportProductSelectors, models.TransientModel, DilveBase):
    _name = "dilve.import.products.wizard"
    _description = "Import products from DILVE"

    dilve_records = fields.Many2many(comodel_name='dilve.record', string='Dilve_records')
    from_date = fields.Datetime(string='Fecha inicio', required=False)
    to_date = fields.Datetime(string='Fecha fin', required=False)
    select_all = fields.Boolean(string='Seleccionar todos', default=False, required=False)

    @api.model
    def default_get(self, fields_list):
        _logger.debug("default_get")
        defaults = super(DilveImportProductsWizard, self).default_get(fields_list)

        defaults['from_date'] = (self.env.context.get("from_date")
                                 or self.env.company.dilve_last_checked
                                 or datetime.today())
        defaults["to_date"] = self.env.context.get("to_date") or datetime.today()

        if "dilve_records" in fields_list:
            dilve_records = self.env.context.get("dilve_records", [])
            if not dilve_records:
                dilve_records = self.get_book_list()

            defaults["dilve_records"] = [(6, 0, dilve_records)]

        return defaults

    @api.onchange('select_all')
    def _onchange_select_all(self):
        value = self.select_all
        for record in self.dilve_records:
            record.is_selected = value

    def refresh_list(self):
        self.dilve_records = self.get_book_list()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dilve.import.products.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            "context": {
                "dilve_records": self.dilve_records.ids,
                "from_date": self.from_date,
                "to_date": self.to_date
            }
        }

    def get_book_list(self):
        _logger.info("Getting book list...")
        records = []
        existing_records = self.get_existing_records()
        for record in existing_records:
            product = self.env["product.template"].search([('isbn_number', '=', record.id.value)])
            if product:
                name = product.display_name
                type = "existing"
            else:
                name = ""
                type = "new"

            dilve_record = self.dilve_records.search([('isbn', '=', record.id.value)])
            if dilve_record:
                dilve_record.write({
                    "name": name,
                    "type": type,
                    "is_selected": False
                })
            else:
                dilve_record = self.env["dilve.record"].create({
                    "isbn": record.id.value,
                    "name": name,
                    "type": type
                })
            records.append(dilve_record.id)

        response = self.get_api().getRecordStatusX(
            from_date=self.from_date or datetime.today(),
            to_date=self.to_date or datetime.today(),
            publisher_code=self.env.company.dilve_publisher_code
        )

        for record in response.changedRecords:
            dilve_record = self.dilve_records.search([('isbn', '=', record.id.value)])
            if dilve_record:
                _logger.debug(f"Found changed book: {dilve_record.isbn}")
                if dilve_record.type != "new":
                    dilve_record.write({
                        "type": "changed"
                    })

        return records

    def get_existing_records(self):
        response = self.get_api().getRecordListX(publisher_code=self.env.company.dilve_publisher_code)
        return response.records

    def import_selected(self):
        isbn_list = [record.isbn for record in self.dilve_records if record.is_selected]
        asyncio.run(self.__import_products(isbn_list))

        self.env.company.dilve_last_checked = datetime.now()
        return {'type': 'ir.actions.client', 'tag': 'reload', }

    async def __import_products(self, isbn_list):
        start_time = time.time()

        _logger.info(f"Starting import of {len(isbn_list)} books...")
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*(self.__import_product(session, isbn) for isbn in isbn_list))

        end_time = time.time()
        elapsed_time = end_time - start_time
        _logger.info("Finished book import")
        _logger.info(f"Importing {len(ret)} books took {elapsed_time:.2f} seconds.")

    async def __import_product(self, session, isbn):
        _logger.info(f"Importing book [{isbn}]...")
        try:
            response = await self.get_api(session).getRecordsX_async(identifier=isbn)
            values = self.map_product(response.onixMessage)

            product = self.env["product.template"].search([('isbn_number', '=', isbn)])

            if product:
                _logger.info(f"Updating book [{isbn}]")

                data = {}
                if self.product_name_selector: data["name"] = values.get("product_name")
                if self.authorship_selector: data["authorship_ids"] = values.get("authorship")
                if self.product_cover_selector: data["image_1920"] = values.get("product_cover")
                if self.tags_selector: data["product_tag_ids"] = values.get("tags")
                if self.pvp_selector: data["list_price"] = values.get("pvp")
                if self.category_selector: data["categ_id"] = values.get("category")
                if self.collections_selector: data["collections"] = values.get("collections")
                if self.taxes_selector: data["taxes_id"] = values.get("taxes")
                if self.weight_selector:
                    data["product_weight"] = values.get("weight")
                    data["weight_uom_id"] = values.get("weight_uom_id")
                if self.length_selector:
                    data["product_length"] = values.get("length")
                    data["dimensional_uom_id"] = values.get("dimensional_uom_id")
                if self.width_selector:
                    data["product_width"] = values.get("width")
                    data["dimensional_uom_id"] = values.get("dimensional_uom_id")
                if self.height_selector:
                    data["product_height"] = values.get("height")
                    data["dimensional_uom_id"] = values.get("dimensional_uom_id")
                if self.page_count_selector:
                    data["page_count"] = values.get("page_count")
                if self.total_copies_selector:
                    data["total_copies"] = values.get("total_copies")

                product.write(data)

                _logger.info(f"Book [{isbn}] updated.")
            else:
                _logger.info(f"Creating book [{isbn}]")

                self.env["product.template"].create({
                    "isbn_number": isbn,
                    "barcode": values.get("barcode"),
                    "name": values.get("product_name"),
                    "authorship_ids": values.get("authorship"),
                    "product_tag_ids": values.get("tags"),
                    "image_1920": values.get("product_cover"),
                    "genera_ddaa": True,
                    "sale_ok": True,
                    "purchase_ok": values.get("category") == self.env.ref("gestion_editorial.product_category_books").id, # True for physical books, false otherwise
                    "list_price": float(values.get("pvp")),
                    "categ_id": values.get("category"),
                    "collections": values.get("collections"),
                    "taxes_id": values.get("taxes"),
                    "type": values.get("type"),
                    "product_weight": values.get("weight"),
                    "weight_uom_id": values.get("weight_uom_id"),
                    "product_length": values.get("length"),
                    "product_width": values.get("width"),
                    "product_height": values.get("height"),
                    # The dimensional_uom_id field is failing to be assigned at creation, it defaults to 'm'
                    # There is an open bug for this --> https://github.com/OCA/product-attribute/issues/2033
                    "dimensional_uom_id": values.get("dimensional_uom_id"),
                    "page_count": values.get("page_count"),
                    "total_copies": values.get("total_copies"),
                })

                _logger.info(f"Book [{isbn}] created.")

        except Exception as e:
            _logger.error(f"Exception importing book [{isbn}]:", exc_info=e)

    def previous_page(self):
        action = self.env.ref("dilve.dilve_import_products_step1_action")
        action_data = action.read()[0]
        action_data["res_id"] = self.id
        return action_data

    def next_page(self):
        action = self.env.ref("dilve.dilve_import_products_step2_action")
        action_data = action.read()[0]
        action_data["res_id"] = self.id
        return action_data