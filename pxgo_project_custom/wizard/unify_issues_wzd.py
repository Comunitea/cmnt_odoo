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


class unify_issues(osv.osv_memory):
    _name = 'unify.issues'
    _description = 'Unify issues'
    _columns = {
        'issues_remove_ids': fields.many2many('project.issue','project_issue_remove', 'remove_issue_id', 'issue_id', 'Issues', required=True),
        'unified_issue_id': fields.many2one('project.issue','Unified issue', required=True)
    }
    def unify_issues(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        form_obj = self.browse(cr, uid, ids, context=context)[0]
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
                self.pool.get('project.issue').write(cr, uid, [form_obj.unified_issue_id.id], {'message_ids': [(6,0,messages)]})
            if issues_to_remove:
                self.pool.get('project.issue').unlink(cr, uid, issues_to_remove)



        return {'type': 'ir.actions.act_window_close'}



unify_issues()
