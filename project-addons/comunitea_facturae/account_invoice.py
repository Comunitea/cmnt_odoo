# -*- coding: utf-8 -*-
# © 2022 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    facturae_start_date = fields.Date()
    facturae_end_date = fields.Date()


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    facturae_start_date = fields.Date(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    facturae_end_date = fields.Date(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
