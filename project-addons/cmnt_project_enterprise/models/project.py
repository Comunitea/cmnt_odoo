# -*- coding: utf-8 -*-

from datetime import date, datetime, time, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    # @api.multi
    # def create_forecast(self):
    #     view_id = self.env.ref('project_forecast.project_forecast_view_form').id
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'project.forecast',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'target': 'current',
    #         'context': {
    #             'default_project_id': self.id,
    #             'default_user_id': self.user_id.id,
    #         }
    #     }


class Task(models.Model):
    _inherit = 'project.task'

    forecast_ids = fields.One2many('project.forecast',
                                    'task_id',
                                    string='Forecasts')

    @api.multi
    def create_forecast_from_deadline(self):
        forecast_obj = self.env['project.forecast']
        date_start = datetime.strftime(datetime.
                                 strptime(self.date_deadline,
                                          '%Y-%m-%d') +
                                 timedelta(days=-self.planned_hours/4),
                                 '%Y-%m-%d')
        _logger.info("date_start=%s", date_start)
        _logger.info("date_end=%s", self.date_deadline)
        forecast_id = forecast_obj.create({
            'project_id': self.project_id.id,
            'task_id': self.id,
            'user_id': self.user_id.id if self.user_id else uid,
            'resource_hours': self.planned_hours,
            'start_date': date_start,
            'end_date': self.date_deadline,
            }
        ).id

        return forecast_id


    @api.multi
    def create_forecast(self):
        view_id = self.env.ref('project_forecast.project_forecast_view_form').id
        date_end = datetime.strftime(datetime.
                                 strptime(self.date_start,
                                          '%Y-%m-%d %H:%M:%S') +
                                 timedelta(days=self.planned_hours/8),
                                 '%Y-%m-%d %H:%M:%S')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.forecast',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                'default_project_id': self.project_id.id,
                'default_task_id': self.id,
                'default_user_id': self.user_id.id,
                'default_resource_hours': self.planned_hours,
                'default_start_date': self.date_start,
                'default_end_date': date_end,
            }
        }
