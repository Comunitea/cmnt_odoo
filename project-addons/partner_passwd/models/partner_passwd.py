# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
import random

import logging
_logger = logging.getLogger(__name__)
# Message appear if Crypto.Cipher is not installed
try:
    from Crypto.Cipher import AES
    from Crypto import Random
except ImportError:
    _logger.info("""You need Crypto.Cipher!
                 install it by using the commando: apt-get install
                 python-crypto """)


class ResPartnerPasswd(models.Model):
    _name = "res.partner.passwd"
    _description = "Password"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    def _encrypt(self, cleartext, key):          # key = uuid
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(cleartext)
        return msg.encode("hex")

    def _decrypt(self, ciphertext, key):
        # You need Crypto.Cipher!
        cipher = AES.new(key, AES.MODE_CFB,
                         ciphertext.decode("hex")[:AES.block_size])
        return cipher.decrypt(ciphertext.decode("hex"))[AES.block_size:]

    def _get_key(self):
        return self.env['ir.config_parameter'].sudo().\
            get_param('database.uuid').replace('-', '')

    def pw_Gen(self, pw_length=15):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./0:;<=>?@[]^_{|}~"
        password = ""
        random.seed()
        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            password = password + alphabet[next_index]
        return password

    @api.one
    def generate_passwd(self):
        """generate new password"""
        self.passwd = self.pw_Gen()
        return True

    service = fields.Many2one('res.partner.service', readonly=True,
                              states={'draft': [('readonly', False)]})
    name = fields.Char(string='Name', index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    passwd = fields.Char(string='Password', index=True, readonly=True,
                         states={'draft': [('readonly', False)]},
                         default=pw_Gen)
    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'),
                              ('cancel', 'Cancelled')], string='Status',
                             index=True, readonly=True, default='draft',
                             track_visibility='onchange', copy=False,
                             help=" * The 'Draft' status is used when the "
                                  "password is editable.\n"
                                  " * The 'Sent' status is used when the "
                                  "password has been sent to the user.\n"
                                  " * The'Cancelled'status is used when "
                                  "the password has been cancelled.\n")
    partner_id = fields.Many2one('res.partner')

    @api.multi
    def send_passwd(self):
        """ Sends the password to the users mail.
        """
        self.ensure_one()
        template = self.env.ref('partner_passwd.email_template_id', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form',
                                    False)
        ctx = dict(
            default_model='res.partner.passwd',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
        )
        self.state = 'sent'
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    @api.returns('ir.ui.view')
    def open_mailform(self):
        """ Update form view id of action to open the invoice """
        return self.env.ref('base.view_partner_form')

    @api.one
    @api.returns('ir.actions.act_window')
    def xopen_mailform(self):
        """ Sends the password to the users mail.
        """

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'view_id': self.env.ref('base.view_partner_form'),
            'res_id': self.id,
            'target': 'new',

        }

    @api.one
    def edit_passwd(self):
        self.state = 'draft'
        return True

    @api.one
    def cancel_passwd(self):
        self.state = 'cancel'
        return True

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        result = super(ResPartnerPasswd, self).read(fields, load)
        for record in result:
            if 'passwd' in record:
                try:
                    record['passwd'] = self._decrypt(record['passwd'],
                                                     self._get_key())
                except TypeError:
                    pass
        return result

    @api.model
    def create(self, vals):
        if 'passwd' in vals:
            vals['passwd'] = self._encrypt(vals['passwd'], self._get_key())
        return super(ResPartnerPasswd, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'passwd' in vals:
            vals['passwd'] = self._encrypt(vals['passwd'], self._get_key())
        return super(ResPartnerPasswd, self).write(vals)


class res_partner(models.Model):
    _inherit = "res.partner"

    passwd_ids = fields.One2many('res.partner.passwd', 'partner_id',
                                 string='Password',
                                 groups="base.group_erp_manager")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
