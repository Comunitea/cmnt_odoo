# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY
#    Pexego Sistemas Informáticos (http://www.pexego.es) All Rights Reserved
#    $Jesús Ventosinos Mayor$
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


{
    'name': 'Project task time control',
    'version': '1.0',
    'category': 'Project management',
    "sequence": 30,
    'complexity': "easy",
    'description': """
        Manages tasks, allowing you  start or stop time counter from the tasks list view.
        When you stop  a task the total working time is stored on it.
    """,
    'author': 'Pexego',
    'website': 'http://www.pexego.es',
    'images': [],
    'depends': ['project'],
    'init_xml': [],
    'update_xml': [
        'project_task.xml',
        'wizard/task_time_control_confirm_wizard.xml',
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'project_data.xml'
    ],
    'demo_xml': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
