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


class ProjectTask(models.Model):
    _inherit = "project.task"

    description = fields.Html()
    sale_id = fields.Many2one(comodel_name='sale.order',
        related='project_id.sale_id',
        string='Sale Order',
        store=True,
        readonly=True,)

    @api.multi
    def write(self, vals):
        stage_id = vals.get('stage_id', False)
        res = super(ProjectTask, self).write(vals)
        ctr = True if 'update' not in self.env.context else \
            self.env.context['update']
        for task in self:
            if vals.get('description', False) and task.issue_id and ctr:
                vals = {'description': vals['description']}
                ctx = self.env.context.copy()
                ctx.update({'update': False})
                task.issue_id.with_context(ctx).write(vals)

            if stage_id and task.issue_id:
                task.issue_id.write({'stage_id': vals['stage_id']})
        return res
