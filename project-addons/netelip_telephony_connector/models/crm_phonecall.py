# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    duration = fields.Float()
    bypassed = fields.Boolean()

    @api.model
    def create(self, vals):
        return super(CrmPhonecall,
                     self.with_context(mail_auto_subscribe_no_notify=1)).\
            create(vals)

    @api.multi
    def write(self, vals):
        return super(CrmPhonecall,
                     self.with_context(mail_auto_subscribe_no_notify=1)).\
            write(vals)
