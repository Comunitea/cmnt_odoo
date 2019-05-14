# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api
from datetime import datetime
from datetime import timedelta


class HrAttendance(models.Model):

    _inherit = 'hr.attendance'

    @api.model
    def cron_attendance_reminder(self):
        for employee in self.env['hr.employee'].search([]):

            currently_working = employee.state == 'present' and True or False
            calendar = employee.calendar_id
            intervals = calendar.get_working_intervals_of_day(
                compute_leaves=True)
            if intervals:
                intervals = intervals[0]
            if currently_working:
                should_be_working = False
                for interval in intervals:
                    if interval[1] > datetime.now() + timedelta(minutes=-calendar.reminder_delay):
                        should_be_working = True
                if not should_be_working:
                    self.env.ref('hr_attendance_reminder.email_template_attendance_reminder').send_mail(employee.id)
                    break
            else:
                for interval in intervals:
                    if interval[1] < datetime.now() or \
                                interval[0] > datetime.now():
                        continue
                    if interval[0] < datetime.now() + timedelta(minutes=-calendar.reminder_delay):
                        self.env.ref('hr_attendance_reminder.email_template_attendance_reminder').send_mail(employee.id)
                        break
