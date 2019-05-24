# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountAnalyticContractLine(models.Model):

    _inherit = "account.analytic.contract.line"

    date_from = fields.Date(
        string='Date From',
        compute='_compute_date_from',
        help='Date from invoiced period',
    )
    date_to = fields.Date(
        string='Date To',
        compute='_compute_date_to',
        help='Date to invoiced period',
    )

    @api.multi
    def _compute_date_from(self):
        # When call from template line.analytic_account_id comodel is
        # 'account.analytic.contract',
        if self._name != 'account.analytic.invoice.line':
            return
        for line in self:
            contract = line.analytic_account_id
            date_start = (
                self.env.context.get('old_date') or fields.Date.from_string(
                    contract.recurring_next_date or fields.Date.today())
            )
            if contract.recurring_invoicing_type == 'pre-paid':
                date_from = date_start
            else:
                date_from = (date_start - contract.get_relative_delta(
                    contract.recurring_rule_type,
                    contract.recurring_interval) + relativedelta(days=1))
            line.date_from = fields.Date.to_string(date_from)

    @api.multi
    def _compute_date_to(self):
        # When call from template line.analytic_account_id comodel is
        # 'account.analytic.contract',
        if self._name != 'account.analytic.invoice.line':
            return
        for line in self:
            contract = line.analytic_account_id
            date_start = (
                self.env.context.get('old_date') or fields.Date.from_string(
                    contract.recurring_next_date or fields.Date.today())
            )
            next_date = (
                self.env.context.get('next_date') or
                date_start + contract.get_relative_delta(
                    contract.recurring_rule_type, contract.recurring_interval)
            )
            if contract.recurring_invoicing_type == 'pre-paid':
                date_to = next_date - relativedelta(days=1)
            else:
                date_to = date_start
            line.date_to = fields.Date.to_string(date_to)
