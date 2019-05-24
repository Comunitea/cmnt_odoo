# -*- coding: utf-8 -*-

{
    'name': 'Contract line dates',
    'version': '10.0.1.0.0',
    'category': 'Contracts',
    'description': """
        Control invoice dates on contract lines for invocing by hours.
        Funcionality backported from contrcat module of 11.0 version
        Credits: OpenERP SA, Tecnativa, LasLabs,
        Odoo Community Association (OCA)"
    """,
    'author': 'Comunitea',
    'website': 'https://www.comunitea.com',
    'depends': ['contract',
                'contract_variable_quantity'],
    'data': ['data/contract_line_qty_formula_data.xml',
             'views/account_analytic_contract_view.xml'],
    'installable': True,
}
