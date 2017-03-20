# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Attendance RFID',
    'version': '8.0.1.0.0',
    'category': 'Human Resources',
    'website': 'http://www.comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'hr',
    ],
    'data': ['security/ir.model.access.csv',
             'views/hr_employee_rfid_key_view.xml',
             'views/hr_employee_rfid_key_log_view.xml',
             'views/hr_employee_view.xml'],
}
