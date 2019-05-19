# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos. All Rights Reserved
#    $Omar Castiñeira Saavedra$
#    $Marta Vázquez Rodríguez$
#    $Javier Colmenero Fernández$
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
from odoo import models, fields, api


class ProjectIssue(models.Model):
    _inherit = "project.issue"

    project_scrum_product_backlog_id = fields.Many2one(
        'project.scrum.product.backlog', 'Backlog')

    @api.multi
    def action_create_task(self):
        """
        Create and a related Task for the visit report, and open it's Form.
        """
        self.ensure_one()
        res = super(ProjectIssue, self).action_create_task()
        task_id = res.get('res_id', False)
        if task_id:
            task_obj = self.env['project.task'].browse(task_id)
            task_obj.description = self.description
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ProjectIssue, self).write(cr, uid, ids, vals,
                                              context=context)
        ctr = True if 'update' not in context else context['update']
        for issue in self.browse(cr, uid, ids, context=context):
            if vals.get('description', False) and issue.task_id and ctr:
                vals = {'description': vals['description']}
                ctx = context.copy()
                ctx.update({'update': False})
                self.pool.get('project.task').write(cr, uid, issue.task_id.id,
                                                    vals, context=ctx)
        return res
