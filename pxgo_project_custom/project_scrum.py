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
from openerp.osv import osv, fields
from openerp import _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class project_scrum_us(osv.osv):
    _inherit = 'project.scrum.us'

    def _calc_to_invoice(self, cr, uid, ids, field_name, args, context=None):
        if context is None:
            context = {}
        res = {}
        bls = self.browse(cr, uid, ids)
        for bl in bls:
            if bl.billable == False:
                amount = 0
            else:
                if bl.point_price ==0:
                    amount = bl.expected_hours/8 * bl.project_id.price_history_point
                else:
                    amount = bl.expected_hours/8 * bl.point_price
            res[bl.id] = amount
        return res

    def _get_project(self, cr, uid, ids, context=None):
        pr_obj = self.pool.get('project.project')
        prs = pr_obj.browse(cr, uid, ids, context=context)

        list_pbls = []
        for pr in prs:
            ids2 = self.pool.get('project.scrum.us').search(cr, uid, [('project_id', '=', pr.id)], context=context)
            list_pbls += ids2

        return list_pbls

    def _get_pbl(self, cr, uid, ids, context=None):
        return ids

    _columns = {
        'billable': fields.boolean('Billable'),
        'invoiced': fields.boolean('Invoiced'),
        'product_id': fields.many2one('product.product', 'Product'),
        'tecnical_notes': fields.text('Technical notes'),
        'point_price': fields.float('Precio PH', help='0 si es precio de proyecto'),
        'to_invoice': fields.function(_calc_to_invoice, method=True, string='Amount invoice', type='float',store={
            'project.project':  (_get_project,
                ['price_history_point', 'fix_by_sprint'],
                10),
            'project.scrum.us':  (_get_pbl,
                ['point_price', 'expected_hours', 'billable'],
                10)})
    }


class project_scrum_sprint(osv.osv):
    _inherit = 'project.scrum.sprint'

    def _calc_to_invoice(self, cr, uid, ids, field_name, args, context=None):
        if context is None:
            context = {}
        res = {}
        sprints = self.browse(cr, uid, ids)
        for sprint in sprints:
            bl_ids = self.pool.get('project.scrum.us').search(cr, uid,[('sprint_id', '=', sprint.id)], context=context)
            bls = self.pool.get('project.scrum.us').browse (cr, uid, bl_ids, context=context)
            amount = 0
            for bl in bls:
                amount += bl.to_invoice
            #Suma una cantidad fija al sprint (Por gestión o por facturación fija )
            if not sprint.no_fix_sum:
                if sprint.fix_by_sprint > 0:
                    amount += sprint.fix_by_sprint
                else:
                    amount += sprint.project_id.fix_by_sprint

            res[sprint.id] = amount
        return res

    def _get_sprint(self, cr, uid, ids, context=None):
        pr_obj = self.pool.get('project.project')
        prs = pr_obj.browse(cr, uid, ids, context=context)

        list_sprints = []
        for pr in prs:
            ids2 = self.pool.get('project.scrum.sprint').search(cr, uid, [('project_id', '=', pr.id)], context=context)
            list_sprints += ids2
        return list_sprints

    def _get_sprint_pbl(self, cr, uid, ids, context=None):
        pbl_obj = self.pool.get('project.scrum.us')
        pbls = pbl_obj.browse(cr, uid, ids, context=context)

        list_sprints = []
        for pbl in pbls:
            list_sprints.append(pbl.sprint_id.id)
        return list_sprints

    def _get_sprints(self, cr, uid, ids, context=None):
        return ids

    def button_validation(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validation'}, context=context)
        for (id, name) in self.name_get(cr, uid, ids):
            message = _("The sprint '%s' is under validation process.") % (name,)
            self.log(cr, uid, id, message)
        return True

    _columns = {
        'no_fix_sum': fields.boolean ('NO sumar importe fijo'),
        'fix_by_sprint': fields.float ('Importe fijo', help ='Si 0, el marcado en proyecto'),
        'to_invoice': fields.function(_calc_to_invoice, method=True, string='Amount to invoice', type='float',store={
            'project.project':  (_get_sprint,
           ['price_history_point', 'fix_by_sprint'],
                10),
            'project_scrum_product_backlog':  (_get_sprint_pbl,
                ['point_price', 'billable', 'expected_hours'],
                10),
            'project.scrum.sprint':  (_get_sprints,
                ['no_fix_sum', 'fix_by_sprint'],
                10),
        }),
        'planned_invoice_date': fields.date('Fecha estimada factura'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('open', 'Open'),
                                   ('pending', 'Pending'),
                                   ('cancel', 'Cancelled'),
                                   ('validation', 'Validation'),
                                   ('done', 'Done')], 'State', required=True),

        'type': fields.selection([('project', 'Proyecto'),
                                ('support', 'Soporte'),
                                ('manage', 'Gestión'),
                                ], 'Type', required=False),


    }
    _defaults = {
        'no_fix_sum': lambda *a: False,
    }


    def onchange_date_stop(self, cr, uid, ids, date_stop=False):
        v = {}
        if date_stop:
            v['planned_invoice_date'] = (datetime.strptime(date_stop, "%Y-%m-%d")
                                         + relativedelta(days=7)).strftime("%Y-%m-%d")
        return {'value': v}

