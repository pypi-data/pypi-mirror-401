# Copyright 2025 - simbiotica.coop
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Suscripciones editoriales",
    "version": "17.0.1.0.1",
    "category": "Suscriptions",
    "summary": "Adds book related functionalities to subscriptions module.",
    "description":"Adds book related functionalities to subscriptions module.",
    "author": "Simbiótica tec S.Coop.Mad.",
    "website": "https://simbiotica.coop/",
    "depends": ["gestion_editorial", "subscription_oca"],
    "data": [
        "data/subscription_data.xml",
        "views/messages/product_added_to_subscriptions.xml",
        "views/add_to_subscriptions_view.xml",
        "views/sale_subscription_form.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}

