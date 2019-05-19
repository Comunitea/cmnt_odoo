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

    issues_remove_ids = fields.\
        Many2many('project.issue', 'project_issue_remove', 'remove_issue_id',
                  'issue_id', 'Issues', required=True)
    unified_issue_id = fields.Many2one('project.issue', 'Unified issue',
                                       required=True)

    @api.multi
    def unify_issues(self):
        self.ensure_one()
        form_obj = self
        issues_to_remove = []
        messages = []
        if form_obj.unified_issue_id:
            if form_obj.unified_issue_id.message_ids:
                for sms in form_obj.unified_issue_id.message_ids:
                    messages.append(sms.id)
            if form_obj.issues_remove_ids:
                for issue_remove in form_obj.issues_remove_ids:
                    if issue_remove.message_ids:
                        for message in issue_remove.message_ids:
                            messages.append(message.id)
                    issues_to_remove.append(issue_remove.id)
            if messages:
                form_obj.unified_issue_id.write({'message_ids':
                                                 [(6, 0, messages)]})
            if issues_to_remove:
                issues_to_remove.unlink()

        return {'type': 'ir.actions.act_window_close'}
