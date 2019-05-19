# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos. All Rights Reserved
#    $Omar Castiñeira Saavedra$
#    $Marta Vázquez Rodríguez$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Customizations in the project models",
    "version" : "1.0",
    "author" : "Pexego",
    "category": "Project Custom",
    "description": """ """,
    'website': 'http://www.pexego.es',
    'init_xml': [],
    "depends" : [
        "base",
        "project",
        "project_issue",
        "project_issue_task",
        "report"
    ],
    'data': [
        "project_issue_view.xml",
        "project_view.xml",
        "data/account_analytic_account_seq.xml",
        "wizard/unify_issues_wzd_view.xml"
    ],
    'test': [],
    'installable': False,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

