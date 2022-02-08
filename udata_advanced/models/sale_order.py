# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    arabic_sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    total_amount_discount = fields.Float(string="Amount Discount", store=True, compute="_compute_amount_discount",
                                   readonly=True)


    @api.depends("order_line")
    def _compute_amount_discount(self):
        for order in self:
            order.total_amount_discount = round(sum(line.amount_discount for line in order.order_line), 2)





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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    amount_discount = fields.Float(string="Amount Discount", store=True, compute="_compute_discount",
                                   readonly=True)


    @api.depends("price_unit", "discount", "product_uom_qty")
    def _compute_discount(self):
        for line in self:
            line.amount_discount = line.discount != 0 and (line.price_unit * line.discount / 100) * line.product_uom_qty or 0




