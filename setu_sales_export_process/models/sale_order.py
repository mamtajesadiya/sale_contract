from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one('setu.sale.contract')
