from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SetuSaleContract(models.Model):
    _name = "setu.sale.contract"
    _description = "SetuSaleContract"
    _rec_name = "number"

    number = fields.Char(string="Number",
                         default=lambda self: self.env['ir.sequence'].next_by_code('setu.sale.contract.sequence'))
    product_package = fields.Char(string="Product Package")
    document = fields.Text(string="Document")
    terms_and_conditions = fields.Text(string="Terms and Conditions ")
    shipment = fields.Text(string="Shipment")
    is_local_contact = fields.Boolean(string="Is Local Contact")
    currency = fields.Many2one('res.currency', string="Currency")
    agreement_date = fields.Date(string="Agreement Date")
    ordering_date = fields.Date(string="Ordering Date")
    delivery_date = fields.Date(string="Delivery Date")
    base_price = fields.Float(string="Base Price")
    quantity = fields.Float(string="Quantity")
    ordered_quantity = fields.Float(string="Ordered Quantity", readonly=True, compute="_compute_quantity")
    company = fields.Many2one('res.company', string="Company")
    customer = fields.Many2one('res.partner', string="Customer")
    commodity = fields.Many2one('product.product', string="Commodity")
    payment_term = fields.Many2one('account.payment.term', string="Payment Term")
    # uoms = fields.Char(string="UOM")
    uom_id = fields.Many2one('uom.uom', compute="_compute_product_uom",
                             domain="[('category_id', '=', product_uom_category_id)]")
    state = fields.Selection(string="State",
                             selection=[('draft', 'Draft'), ('ongoing', 'Ongoing'),
                                        ('close', 'Close'), ('cancel', 'Cancel')],
                             default='draft')
    sale_order_ids = fields.One2many('sale.order', 'contract_id')
    sale_order_count = fields.Integer(compute="_compute_sale_order")
    product_uom_category_id = fields.Many2one(related='commodity.uom_id.category_id', depends=['commodity'])

    def close(self):
        if self.state != 'close':
            self.state = 'close'

    def cancel(self):
        if self.state != 'cancel':
            self.state = 'cancel'

    @api.depends('commodity')
    def _compute_product_uom(self):
        for line in self:
            if not line.uom_id or (line.commodity.uom_id.id != line.uom_id.id):
                line.uom_id = line.commodity.uom_id

    @api.depends('sale_order_ids')
    def _compute_quantity(self):
        self.ordered_quantity = 0
        for rec in self:
            sale = self.env['sale.order'].search([('contract_id', '=', rec.mapped('id'))])
            if sale:
                for record in sale:
                    if record.state == 'draft':
                        rec.ordered_quantity += record.order_line.product_uom_qty
            else:
                rec.ordered_quantity = 0

    @api.depends('sale_order_ids')
    def _compute_sale_order(self):
        self.sale_order_count = len(self.sale_order_ids)

    def check_sale_order(self):
        sale_order = self.env['sale.order'].search([('contract_id', '=', self.id)])
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'name': 'Sale Order',
            # 'domain': [('id', 'in', sale_order.ids)]
            # 'res_id': sale_order.ids
        }
        if self.sale_order_count == 1:
            action.update({
                'view_mode':'form',
                'res_id': sale_order.id
            })
        else:
            action.update({
                'view_mode':'tree,form',
                'domain': [('id', 'in', sale_order.ids)]
            })
        return action

    def confirm(self):
        if self.state != 'ongoing':
            self.state = 'ongoing'



