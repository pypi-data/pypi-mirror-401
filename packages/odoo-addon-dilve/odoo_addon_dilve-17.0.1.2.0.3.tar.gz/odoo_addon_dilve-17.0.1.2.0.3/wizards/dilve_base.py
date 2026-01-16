import io
import logging
import base64
from PIL import Image, ImageOps

from ..dapi import dapi, dapi_mock
from ..dapi.thema import Thema
from ..onix.onix_book_product_code_lists import List23, List58
from ..onix.onix2odoo import UnnamedPersons, ContributorRole, MeasureType, MeasureUnit

_logger = logging.getLogger(__name__)

DEBUG = False

class DilveBase:

    def get_api(self, session=None):
        if not hasattr(self, 'api'):
            company = self.env.company
            if not DEBUG:
                self.api = dapi.DapiClient(
                    user=company.dilve_user,
                    pswd=company.dilve_pass,
                    session=session
                )
            else:
                self.api = dapi_mock.DapiClient()

        return self.api

    def map_product(self, onix_message):
        self.__onix_message = onix_message

        barcode = self.__get_barcode()
        self.existing_product = self.env["product.template"].search([("barcode", "=", barcode)])

        weight, weight_uom_id = self.__get_measure(MeasureType.WEIGHT)
        length, length_uom_id = self.__get_measure(MeasureType.HEIGHT)
        width, width_uom_id = self.__get_measure(MeasureType.WIDTH)
        height, height_uom_id = self.__get_measure(MeasureType.THICKNESS)

        return {
            "product_name": self.__get_title(),
            "barcode": barcode,
            "authorship": self.__get_authorships(),
            "tags": self.__get_tags(),
            "product_cover": self.__get_product_cover(barcode),
            "pvp": self.__get_product_price(),
            "category": self.__get_category(),
            "taxes": self.__get_taxes(),
            "type": self.__get_type(),
            "weight": weight,
            "weight_uom_id": weight_uom_id,
            "length": length,
            "width": width,
            "height": height,
            "dimensional_uom_id": height_uom_id,
            "collections": self.__get_collections(),
            "page_count": self.__get_page_count(),
            "total_copies": self.__get_total_copies(),
        }


    def __get_title(self):
        product = self.__onix_message.product[0]
        return product.descriptive_detail.title_detail[0].title_element[0].title_text[0].value

    def __get_barcode(self):
        product = self.__onix_message.product[0]
        return product.record_reference.value

    def __get_authorships(self):
        authorships = []
        product = self.__onix_message.product[0]
        contributors = product.descriptive_detail.contributor
        for contributor in contributors:
            for role in contributor.contributor_role:
                values = {}
                if self.existing_product:
                    values["product_id"] = self.existing_product.id

                editorial_role = self.env.ref(ContributorRole.get_reference(role.value)).id
                values["contact_type"] = editorial_role

                name = self.__get_contact_name(contributor)
                contact = self.env["res.partner"].search([("name", "=", name)])
                if contact:
                    contact.write({
                        "name": name,
                        "is_author": True
                    })
                    values["author_id"] = contact.id

                    authorship = self.env["authorship.product"].search([
                        ("product_id", "=", values.get("product_id")),
                        ("author_id", "=", values.get("author_id")),
                        ("contact_type", "=", values.get("contact_type")),
                    ])

                    if authorship:
                        authorships.append((4, authorship.id, values))
                        break

                else:
                    values["author_id"] = self.env["res.partner"].create({
                        "name": name,
                        "is_author": True
                    }).id

                authorships.append((0, 0, values))
        return authorships

    def __get_contact_name(self, contributor):
        if contributor.unnamed_persons:
            name = UnnamedPersons.get_display_name(contributor.unnamed_persons[0].value)
        else:
            name_inverted = contributor.person_name_inverted[0].value
            try:
                last_name, first_name = name_inverted.split(', ')
                name = f"{first_name} {last_name}"
            except ValueError:
                name = name_inverted
        return name

    def __get_category(self):
        product = self.__onix_message.product[0]
        product_form = product.descriptive_detail.product_form
        if product_form.value.value[0] == "B":
            return self.env.ref("gestion_editorial.product_category_books").id
        elif product_form.value.value[0] == "E":
            return self.env.ref("gestion_editorial.product_category_digital_books").id

    def __get_tags(self):
        try:
            tags = []
            thema = Thema()
            product = self.__onix_message.product[0]
            subjects = product.descriptive_detail.subject
            for subject in subjects:
                if subject.subject_code:
                    tag_name = thema.get_from_code(subject.subject_code.value)
                    if tag_name:
                        tag = self.env["product.tag"].search([('name', '=', tag_name)])
                        if not tag:
                            tag = self.env["product.tag"].create({
                                "name": tag_name
                            })
                        tags.append(tag.id)

            return tags
        except Exception as e:
            _logger.error(f"Exception: {e}")

    def __get_product_cover(self, barcode):
        product =  self.__onix_message.product[0]
        cover_url = product.collateral_detail.supporting_resource[0].resource_version[0].resource_link[0].value
        try:
            cover_url = cover_url.lstrip("file://")
            cover = self.get_api().getResourceX(barcode, cover_url).resource
            if cover:
                image_compressed = self.__compress_image(cover)
                return base64.b64encode(image_compressed)
            else:
                return None
        except OSError as e:
            _logger.error(e)
            return None

    def __compress_image(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        base_width = 300
        wpercent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image_resized = image.resize((base_width, hsize), Image.LANCZOS)
        buffered = io.BytesIO()
        image_resized.save(buffered, format="JPEG")
        return buffered.getvalue()

    def __get_product_price(self, include_taxes=False):
        _logger.debug(f"Include Taxes: {include_taxes}")
        product = self.__onix_message.product[0]
        price = product.product_supply[0].supply_detail[0].price[0]

        # If price_type includes taxes
        if price.price_type.value in (List58.VALUE_02, List58.VALUE_04, List58.VALUE_07, List58.VALUE_09,
                                      List58.VALUE_12, List58.VALUE_14, List58.VALUE_17, List58.VALUE_22,
                                      List58.VALUE_24, List58.VALUE_27, List58.VALUE_34, List58.VALUE_42):
            if not include_taxes:
                return price.tax[0].taxable_amount[0].value # Get product price excluding taxes

        return price.price_amount.value # Get product price including taxes

    def __get_taxes(self):
        try:
            taxes = []
            product = self.__onix_message.product[0]
            tax_rate_percent = int(product.product_supply[0].supply_detail[0].price[0].tax[0].tax_rate_percent.value)
            if tax_rate_percent == 4:
                taxes.append(self.env.ref("account.1_account_tax_template_s_iva4b").id)
            elif tax_rate_percent == 10:
                taxes.append(self.env.ref("account.1_account_tax_template_s_iva10b").id)
            elif tax_rate_percent == 21:
                taxes.append(self.env.ref("account.1_account_tax_template_s_iva21b").id)

            return taxes
        except Exception as e:
            _logger.error(e)

    def __get_type(self):
        category = self.__get_category()
        if category == self.env.ref("gestion_editorial.product_category_books").id:
            return "product"

        if category == self.env.ref("gestion_editorial.product_category_digital_books").id:
            return "consu"

        return "product"

    def __get_measure(self, type):
        product = self.__onix_message.product[0]
        measures = product.descriptive_detail.measure
        for measure in measures:
            _logger.debug(f"Measure: {measure}")
            if measure.measure_type.value == type.value:
                measure_unit = self.__get_measure_unit(measure)
                return measure.measurement.value, measure_unit
        return None, None

    def __get_measure_unit(self, measure):
        return self.env.ref(MeasureUnit.get_reference(measure.measure_unit_code.value)).id

    def __get_collections(self):
        product = self.__onix_message.product[0]
        dilve_collections = product.descriptive_detail.collection
        collection_ids = []

        for dilve_collection in dilve_collections:
            name = dilve_collection.title_detail[0].title_element[0].title_text[0].value
            if name:
                collection = self.env["product.template.collection"].search([('name', '=', name)])
                if not collection:
                    collection = self.env["product.template.collection"].create({
                        "name": name
                    })
                collection_ids.append(collection.id)

        return collection_ids

    def __get_page_count(self):
        product = self.__onix_message.product[0]
        extents = product.descriptive_detail.extent
        for extent in extents:
            _logger.debug(f"Extent: {extent}")
            if extent.extent_type.value == List23.VALUE_00:
                return extent.extent_value.value
        return None

    def __get_total_copies(self):
        product = self.__onix_message.product[0]
        reprint_detail = product.product_supply[0].market_publishing_detail.reprint_detail

        total_copies = 0
        if reprint_detail:
            # reprint_detail has the following structure: "[1;20200226;1000|2;20200715;1000]" as "edition;date;copies"
            content = reprint_detail[0].content
            editions = content[0].split('|')
            for edition in editions:
                try:
                    copies = edition.split(';')[2]
                    total_copies += int(copies)
                except ValueError as e:
                    _logger.warning(e)

        return total_copies