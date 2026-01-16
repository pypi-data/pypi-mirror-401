import logging
from odoo import api, fields, models, exceptions
from odoo.osv import expression
from markupsafe import Markup

_logger = logging.getLogger(__name__)

class AddToSubscriptionsWizard(models.TransientModel):
    _name = "subscriptions.wizard"
    _description = "Add to subscriptions wizard"

    product = fields.Many2one(comodel_name="product.template", string="Product", required=True)

    subscription_templates = fields.Many2many(
        comodel_name='sale.subscription.template',
        string='Plantillas de suscripción'
    )

    @api.model
    def _subscriber_domain(self):
        subscribers_ids = self.env["sale.subscription"].search([('in_progress', '=', 'true')]).mapped("partner_id").ids
        return [("id", "in",subscribers_ids)]

    subscriber = fields.Many2many(
        comodel_name='res.partner',
        string='Suscriptora',
        domain=_subscriber_domain
    )

    subscriptions = fields.Many2many(
        comodel_name="sale.subscription",
        compute="_compute_subscriptions",
        string="Subscriptions"
    )

    @api.depends("subscription_templates", "subscriber")
    def _compute_subscriptions(self):
        for record in self:
            domain = [
                "&",
                ('in_progress', '=', 'true'),
                "|",
                ('template_id', 'in', self.subscription_templates.ids),
                ('partner_id', 'in', self.subscriber.ids)
            ]
            record.subscriptions = self.env["sale.subscription"].search(domain)


    def add_product_to_subscription(self):
        product = self.product
        location_id = self.env.ref("stock.stock_location_stock").id
        location_dest_id = self.env.ref("stock.stock_location_customers").id

        for subscription in self.subscriptions:
            subscription.related_products = [(4, product.id)] # Add product to subscription's related_products

            # Create delivery order
            stock_picking = self.env['stock.picking'].create({
                'partner_id': subscription.partner_id.id,
                'picking_type_id': self.env.ref("editorial_subscriptions.stock_picking_type_subscription").id,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
                "move_type": "direct",
                "origin": subscription.name,
            })
            _logger.debug("stock.picking created.")

            _logger.debug("Creating stock.move")
            stock_move = self.env['stock.move'].create({
                'picking_id': stock_picking.id,
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': 1,
                'product_uom': product.uom_id.id,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
            })
            _logger.debug("stock.move created.")

            stock_picking.action_confirm()

            # Add note in stock_picking record
            stock_picking.message_post_with_source(
                "mail.message_origin_link",
                subtype_xmlid="mail.mt_note",
                render_values={"self": stock_picking, "origin": subscription},
            )

            # Add note in subscription record
            subscription.message_post_with_source(
                "editorial_subscriptions.product_added_to_subscriptions",
                subtype_xmlid="mail.mt_note",
                render_values={"product": product, "move": stock_picking},
            )

        # Add note in product record
        product.message_post_with_source(
            "editorial_subscriptions.product_added_to_subscriptions",
            subtype_xmlid="mail.mt_note",
            render_values={"subscriptions": self.subscriptions},
        )
