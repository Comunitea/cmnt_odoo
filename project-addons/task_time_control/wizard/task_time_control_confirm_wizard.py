# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY
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

from odoo import fields, models, api
import time


class TaskTimeControlConfirmWizard(models.TransientModel):
    _name = 'task.time.control.confirm.wizard'

    @api.multi
    def getUserTask(self):
        user = False
        user = self.env['time.control.user.task'].\
            search([('user', '=', self.env.user.id)], limit=1)
        return user

    @api.multi
    def see_started_tasks(self):
        user = self.getUserTask()
        return (user and user.started_task.id or False)

    @api.multi
    def get_time(self):
        user = self.getUserTask()
        if user:
            start_datetime = fields.Datetime.from_string(user.work_start)
            end_datetime = fields.Datetime.from_string(user.work_end)
            end_seconds = time.mktime(end_datetime.timetuple())
            start_seconds = time.mktime(start_datetime.timetuple())
            diff_hours = (end_seconds - start_seconds)/60/60
        return (user and diff_hours or 0.00)

    task_to_start = fields.Many2one('project.task', 'Task to init')
    user_task = fields.Many2one('time.control.user.task', 'User task')
    started_task = fields.Many2one('project.task', 'Started Task',
                                   default=see_started_tasks)
    name = fields.Char('Name', size=128)
    ttime = fields.Float('Time', oldname="time", default=get_time)

    @api.multi
    def close_confirm(self):
        self.ensure_one()
        wizard = self
        user_task = wizard.user_task
        started_task = user_task.started_task
        start_datetime = user_task.work_start
        end_datetime = user_task.work_end
        args = {
            'name': wizard.name,
            'date': end_datetime,
            'task_id': started_task.id,
            'unit_amount': wizard.ttime,
            'user_id': self.env.user.id,
            'project_id': started_task.project_id.id,
            'company_id': started_task.company_id and
            started_task.company_id.id or False,
            'work_start': start_datetime,
            'work_end': end_datetime
         }
        self.env["account.analytic.line"].create(args)
        user_task.write({'work_start': None,
                         'work_end': None,
                         'started_task': None})
        other_users_in_task = self.env['time.control.user.task'].\
            search([('started_task', '=', started_task.id)])
        if not other_users_in_task:
            #TOCHECK
            ttype = started_task.stage_find([('name', 'ilike', '%devel%')])
            started_task.write({'stage_id': ttype})
        if wizard.task_to_start:
            start_id = wizard.task_to_start
            #TOCHECK
            ttype = started_task.stage_find([('name', 'ilike', '%working%')])
            start_id.write({'stage_id': ttype})
            user_task.write({'work_start': end_datetime,
                             'started_task': start_id.id})
        return {'type': 'ir.actions.act_window_close'}
