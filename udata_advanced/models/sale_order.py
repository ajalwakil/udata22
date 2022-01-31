# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    arabic_sale_terms_and_conditions = fields.Text(string='Terms and Conditions')


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


