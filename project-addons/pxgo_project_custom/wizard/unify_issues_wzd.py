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
from odoo import models, fields, api


class UnifyIssues(models.TransientModel):
    _name = 'unify.issues'
    _description = 'Unify issues'

    @api.model
    def default_get(self, fields):
        rec = super(UnifyIssues, self).default_get(fields)
        if self.env.context.get('active_ids'):
            rec.update({'issues_remove_ids':
                        [(6, 0, self.env.context['active_ids'])]})
        return rec

    issues_remove_ids = fields.\
        Many2many('project.issue', 'project_issue_remove', 'remove_issue_id',
                  'issue_id', 'Issues', required=True)
    unified_issue_id = fields.Many2one('project.issue', 'Unified issue',
                                       required=True)

    @api.multi
    def unify_issues(self):
        self.ensure_one()
        form_obj = self
        issues_to_remove = form_obj.issues_remove_ids - \
            form_obj.unified_issue_id
        messages = self.env['mail.message'].\
            search([('res_id', 'in', form_obj.issues_remove_ids.ids),
                    ('res_id', '!=', form_obj.unified_issue_id.id),
                    ('model', '=', 'project.issue')])
        messages.write({'res_id': form_obj.unified_issue_id.id})
        if issues_to_remove:
            issues_to_remove.unlink()

        return {'type': 'ir.actions.act_window_close'}
