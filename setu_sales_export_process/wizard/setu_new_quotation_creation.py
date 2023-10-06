from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class SetuNewQuotationCreation(models.TransientModel):
    _name = "setu.new.quotation.creation"
    _description = "SetuNewQuotationCreation"

    customer = fields.Many2one('res.partner', string="Customer")
    partners = fields.Many2one('res.partner',string="Partner")
    fright_price = fields.Float(string="Fright Price")
    base_price = fields.Float(string="Base Price")
    quantity = fields.Float(string="Quantity")
    setu_sale_contract_id = fields.Many2one('setu.sale.contract', string="Contract")
    uom = fields.Many2one('uom.uom', string="UOM")

    @api.constrains('quantity')
    def _check_quantity(self):
        con = self.env['setu.sale.contract'].browse(self._context.get('active_id'))
        if self.quantity > con.quantity - con.ordered_quantity or self.quantity == 0:
            raise ValidationError("You need to enter quantity less than actual quantity")

    @api.model
    def default_get(self, fields):
        con = self.env['setu.sale.contract'].browse(self._context.get('active_id'))
        if con.quantity <= con.ordered_quantity:
            raise ValidationError("There is no quantity so can not create sale order")
        res = super(SetuNewQuotationCreation, self).default_get(fields)
        contract = self.env['setu.sale.contract'].browse(self._context.get('active_id'))
        res['partners'] = contract.customer
        res['base_price'] = contract.base_price
        res['quantity'] = contract.quantity
        res['uom'] = contract.uom_id.id
        return res

    def create_sale_order(self):
        contract = self.env['setu.sale.contract'].browse(self._context.get('active_id'))
        sale_order = self.env['sale.order'].create({'company_id': contract.company.id,
                                                    'partner_id': self.customer.id,
                                                    'payment_term_id': contract.payment_term.id,
                                                    'currency_id': contract.currency.id,
                                                    # 'state': contract.state,
                                                    'contract_id': contract.id,
                                                    'order_line': [Command.create({'product_id': contract.commodity.id,
                                                                                   'name': contract.commodity.id,
                                                                                   'product_uom': contract.uom_id.id,
                                                                                   'product_uom_qty': self.quantity,
                                                                                   'price_unit': self.fright_price+self.base_price
                                                                                   })]

                                                    })


