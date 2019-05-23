# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019 Comunitea All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from odoo import models, fields, api


class ResCompany(models.Model):

    _inherit = "res.company"

    netelip_api_key = fields.Char("Netelip API Key")
    netelip_webdav_hostname = fields.Char("Netelip Webdav Host")
    netelip_webdav_login = fields.Char("Netelip Webdav Login")
    netelip_webdav_password = fields.Char("Netelip Webdav Password")
    netelip_phone = fields.Char("Netelip Phone")


class BaseConfigSettings(models.TransientModel):

    _inherit = 'base.config.settings'

    netelip_api_key = fields.Char("Netelip API Key",
                                  default=lambda s: s.env.user.company_id.
                                  netelip_api_key)
    netelip_webdav_hostname = fields.Char("Netelip Webdav Host",
                                          default=lambda s: s.env.user.
                                          company_id.netelip_webdav_hostname)
    netelip_webdav_password = fields.Char("Netelip Webdav Password",
                                          default=lambda s: s.env.user.
                                          company_id.netelip_webdav_password)
    netelip_webdav_login = fields.Char("Netelip Webdav Login",
                                       default=lambda s: s.env.user.
                                       company_id.netelip_webdav_login)
    netelip_phone = fields.Char("Netelip Phone",
                                default=lambda s: s.env.user.
                                company_id.netelip_phone)

    @api.multi
    def set_netelip_api_key(self):
        self.env.user.company_id.netelip_api_key = self.netelip_api_key

    @api.multi
    def set_netelip_webdav_hostname(self):
        self.env.user.company_id.netelip_webdav_hostname = \
            self.netelip_webdav_hostname

    @api.multi
    def set_netelip_webdav_login(self):
        self.env.user.company_id.netelip_webdav_login = \
            self.netelip_webdav_login

    @api.multi
    def set_netelip_webdav_password(self):
        self.env.user.company_id.netelip_webdav_password = \
            self.netelip_webdav_password

    @api.multi
    def set_netelip_phone(self):
        self.env.user.company_id.netelip_phone = self.netelip_phone
