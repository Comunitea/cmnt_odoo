# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Password Manager',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'description': """
Adds a tab for managing passwords to Customers. Passwords are
automaticly encrypted before being written to the database, and
decrypted when read.
===================================================
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base', 'mail'],
    'data': ['views/partner_view.xml',
             'security/ir.model.access.csv'],
    'external_dependencies': {
        'python': ['crypto'],
    },
    'installable': True,

}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
