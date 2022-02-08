# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    arabic_sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    total_amount_discount = fields.Float(string="Amount Discount", store=True, compute="_compute_amount_discount",
                                   readonly=True)
    next_number = fields.Integer(default=1,copy=False)
    sale_reversion_id = fields.Many2one(comodel_name="sale.order")
    versioned = fields.Boolean(copy=False)

    sale_order_ids = fields.One2many(comodel_name="sale.order", inverse_name="sale_reversion_id",  string="Sales Orders", required=False, readonly=1)


    def _compute_amount_discount(self):
        for order in self:
            amount_discount =  0
            for line in self.order_line:
                amount_discount = line.discount != 0 and (line.price_unit * line.discount / 100) * line.product_uom_qty or 0
            order.total_amount_discount = round(amount_discount, 2)


    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        sale_terms_and_conditions = self.env["ir.config_parameter"].sudo().get_param(
            "udata_advanced.sale_terms_and_conditions", False)
        arabic_sale_terms_and_conditions = self.env["ir.config_parameter"].sudo().get_param(
            "udata_advanced.arabic_sale_terms_and_conditions", False)
        res.update({
            'sale_terms_and_conditions': sale_terms_and_conditions or False,
            'arabic_sale_terms_and_conditions': arabic_sale_terms_and_conditions or False,
                    })
        return res



    def _get_url_order(self):
        return 'https://udata22.odoo.com' + self.get_portal_url()


    def action_reversion(self):
        if self.state not in ['draft', 'sent']:
            return
        history_order = self.copy()
        history_order.name = self.name + " - " + str(self.next_number)
        self.sale_reversion_id = history_order.id
        self.next_number += 1
        self.versioned = True
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': history_order.id,
            'type': 'ir.actions.act_window',
        }
        return history


    # def action_reversion(self):
    #     if self.state not in ['draft', 'sent']:
    #         return
    #     lines = []
    #     for line in self.order_line:
    #
    #         lines.append((0, 0, line._prepare_line(self.id)))
    #     print("lines", lines)
    #     history_order = self.env["sale.order.history"].sudo().create(
    #         {
    #             'name': self.name + " - " + str(self.next_number),
    #             'origin': self.origin,
    #             'client_order_ref': self.client_order_ref,
    #             'reference': self.reference,
    #             'state': self.state,
    #             'date_order': self.date_order,
    #             'validity_date': self.validity_date,
    #             'is_expired': self.is_expired,
    #             'require_signature': self.require_signature,
    #             'require_payment': self.require_payment,
    #             'partner_id': self.partner_id.id,
    #             'partner_invoice_id': self.partner_invoice_id.id,
    #             'partner_shipping_id': self.partner_shipping_id.id,
    #             'pricelist_id': self.pricelist_id.id,
    #             'currency_id': self.currency_id.id,
    #             'analytic_account_id': self.analytic_account_id.id,
    #             'order_line': lines,
    #             'payment_term_id': self.payment_term_id.id,
    #             'user_id': self.user_id.id,
    #             'sale_reversion_id': self.id,
    #         },
    #
    #     )
    #     self.next_number += 1
    #     self.versioned = True
    #     return {
    #         'context': self.env.context,
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'sale.order',
    #         'res_id': history_order.id,
    #         'type': 'ir.actions.act_window',
    #     }
    #
    #     return history



# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     def _prepare_line(self):
#         """
#         Prepare the dict of values to create the new invoice line for a sales order line.
#
#         :param qty: float quantity to invoice
#         :param optional_values: any parameter that should be added to the returned invoice line
#         """
#         self.ensure_one()
#         res = {
#             'display_type': self.display_type,
#             'sequence': self.sequence,
#             'name': self.name,
#             'product_id': self.product_id.id,
#             'product_uom_qty': self.product_uom.id,
#             'quantity': self.qty_to_invoice,
#             'discount': self.discount,
#             'price_unit': self.price_unit,
#             'tax_ids': [(6, 0, self.tax_id.ids)],
#             'analytic_account_id': self.order_id.analytic_account_id.id,
#             'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
#
#         }
#
#         return res
#
#
#
#
#
#
