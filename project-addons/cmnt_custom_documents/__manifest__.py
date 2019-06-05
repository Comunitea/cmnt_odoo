# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Customizations in report for Comunitea',
    'version': '10.0.1.0.0',
    'summary': '',
    'category': 'Reporting',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'account'
    ],
    'data': ['views/report_invoice.xml',
             'views/report_sale.xml',
             'views/sale_view.xml'],
    'installable': True,
}
