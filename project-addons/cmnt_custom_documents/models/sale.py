# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    show_subtotals = fields.Boolean("Show subtotals in report")
