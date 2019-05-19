# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Pexego Sistemas Informáticos (http://www.pexego.es) All Rights Reserved
#    $Jesús Ventosinos Mayor$
#    $Javier Colmenero Fernández$
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

from odoo import fields, _, exceptions, models, api


class TimeControlUserTask(models.Model):
    _name = 'time.control.user.task'

    user = fields.Many2one('res.users', 'User')
    work_start = fields.Datetime('Work start')
    work_end = fields.Datetime('Work end')
    started_task = fields.Many2one('project.task', 'Started task')


class ProjectTask(models.Model):

    @api.multi
    def _get_users_working(self):
        for task in self:
            stream = ''
            user_in_task = self.env["time.control.user.task"].\
                search([('started_task', '=', task.id)])
            for usr in user_in_task:
                if usr.user.name:
                    stream += usr.user.name + u","
            task.working_users = stream

    _inherit = "project.task"

    other_users_ids = fields.Many2many('res.users', 'project_task_user_rel',
                                       'user_id', 'task_id', 'Other users')
    working_users = fields.Char('Working users', compute="_get_users_working",
                                size=255)

    @api.model
    def stop_task(self, task_id, final, user_task):
        user_task.write({'work_end': final})
        wizard_id = self.env["task.time.control.confirm.wizard"].\
            create({'task_to_start': task_id,
                    'user_task': user_task.id})
        return {
            'name': _("Confirm Time"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'task.time.control.confirm.wizard',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': self.env.context
        }

    @api.multi
    def work_start_btn(self):
        self.ensure_one()
        start = fields.Datetime.now()
        start = fields.Datetime.from_string(start)
        user_task = self.env['time.control.user.task'].\
            search([('user', '=', self.env.user.id)], limit=1)
        task = self[0]
        if user_task:
            if user_task.started_task:
                if user_task.started_task.id == task.id:
                    raise exceptions.UserError(_("Task is alredy started."))
                return task.stop_task(start, user_task)
            else:
                #TOCHECK
                ttype = task.stage_find([('name', 'ilike', '%working%')])
                task.write({'stage_id': ttype})
                user_task.write({'work_start': start,
                                 'started_task': task.id})
        else:
            args = {
                'user': self.env.user.id,
                'work_start': start,
                'started_task': task.id
            }
            self.env['time.control.user.task'].create(args)
            #TOCHECK
            ttype = task.stage_find([('name', 'ilike', '%working%')])
            task.write({'stage_id': ttype})
        return True

    @api.multi
    def work_end_btn(self):
        self.ensure_one()
        end_datetime = fields.Datetime.now()
        end_datetime = fields.Datetime.from_string(end_datetime)
        user_task = self.env['time.control.user.task'].\
            search([('user', '=', self.env.user.id)], limit=1)
        if user_task:
            if user_task.started_task.id == self.id:
                finished = self.stop_task(None, end_datetime, user_task)
                if finished:
                    return finished
                else:
                    raise exceptions.UserError(_('Task is not init.'))
            else:
                raise exceptions.UserError(_('Task init by another user.'))
        return True


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    work_start = fields.Datetime('Work start')
    work_end = fields.Datetime('Work end')
