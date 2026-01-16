from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class EditorialSubscription(models.Model):
    """ Extend sale.subscription template for editorial management """
    _description = "Editorial Subcription"
    _inherit = 'sale.subscription'

    related_products = fields.Many2many(
        comodel_name='product.template',
        string='Related products'
    )


    def action_open_product(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.template',
            'res_id': self.id,
        }

