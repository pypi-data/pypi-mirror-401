# Copyright 2025 - simbiotica.coop
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "DILVE",
    "version": "17.0.1.2.0",
    "category": "Products",
    "summary": "Módulo para la integración con el sistema DILVE.",
    "description": "Módulo para la integración con el sistema DILVE.",
    "author": "Simbiótica tec S.Coop.Mad.",
    "website": "https://simbiotica.coop/",
    "depends": ["gestion_editorial", ],
    "external_dependencies": {"python": [
        "xmlschema",
        "xsdata[cli]",
        "aiohttp"
    ]},
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/dilve_import_product_view.xml",
        "views/dilve_import_products_step1_view.xml",
        "views/dilve_import_products_step2_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "/dilve/static/src/xml/import_from_dilve_button.xml",
            "/dilve/static/src/js/import_from_dilve_button.js",
        ]
    },
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}

