# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderHistory(models.Model):
    _name = 'sale.order.history'
    _inherit = 'sale.order'


    transaction_ids = fields.Many2many('payment.transaction', 'sale_order_rel', 'sale_id', 'transaction_id',
                                       string='Transactions', copy=False, readonly=True)

    tag_ids = fields.Many2many('crm.tag', 'sale_tag_rel', 'order_id', 'tag_id', string='Tags')

    order_line = fields.One2many('sale.order.history.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)




class SaleOrderHistoryLine(models.Model):
    _name = 'sale.order.history.line'
    _inherit = 'sale.order.line'


    invoice_lines = fields.Many2many('account.move.line', 'sale_order_line_rel', 'order_line_id', 'invoice_line_id', string='Invoice Lines', copy=False)


