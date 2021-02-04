# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta


class ProjectProject(models.Model):

    _inherit = "project.project"

    okr_project = fields.Boolean()


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.multi
    def _get_okr_progress(self):
        for task in self:
            if task.key_result_ids:
                length = len(task.key_result_ids)
                value = sum(task.key_result_ids.mapped('progress'))
                progress = round((value / length), 2)
                task.okr_progress = progress
                if progress < 75.0 and task.date_end:
                    warning_date = datetime.\
                        strftime(datetime.
                                 strptime(task.date_end,
                                          '%Y-%m-%d %H:%M:%S') +
                                 timedelta(days=-30), '%Y-%m-%d %H:%M:%S')
                    if fields.Date.today() < warning_date:
                        task.warning = True

    okr_project = fields.Boolean()
    key_result_ids = fields.One2many('project.key.result', 'task_id',
                                     "Key results", copy=True)
    okr_progress = fields.Float("Progress", digits=(16, 2),
                                compute="_get_okr_progress")
    warning = fields.Boolean(compute="_get_okr_progress")

    @api.onchange('project_id')
    def _onchange_project(self):
        super(ProjectTask, self)._onchange_project()
        if self.project_id:
            self.okr_project = self.project_id.okr_project

    @api.multi
    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if 'active' in vals:
            self.with_context(active_test=False).mapped('key_result_ids').\
                write({'active': vals['active']})
        return res


class ProjectFollowType(models.Model):

    _name = "project.follow.type"

    name = fields.Char("Description", required=True)


class ProjectKeyResult(models.Model):

    _name = "project.key.result"

    @api.multi
    def _get_result(self):
        for res in self:
            result = False
            res.failed = False
            if res.compute_type == "manual":
                objs = res.manual_input_ids
                if objs:
                    result = sum(objs.mapped('value'))
            else:
                eval_dict = {'task': res.task_id}
                try:
                    domain = eval(res.automatic_domain, eval_dict)
                    objs = self.env[res.automatic_model].sudo().search(domain)
                except Exception:
                    res.failed = True
                    objs = []

                if objs and res.compute != 'count':
                    result = sum(objs.mapped(res.automatic_field))
                else:
                    result = len(objs)
            if result:
                if res.compute == "avg":
                    result = round(result / len(objs), 2)
                res.result = result
                if (res.expected_result > 0.0):
                    res.progress = round(100.0 * result /
                                         res.expected_result, 2)
                else:
                    res.progress = 0.0

    name = fields.Char("Description", required=True)
    task_id = fields.Many2one("project.task", "Task", ondelete="restrict")
    expected_result = fields.Float("Expected Result", digits=(16, 2))
    compute_type = fields.Selection([('auto', 'Automatic'),
                                     ('manual', 'Manual')], "Compute type",
                                    required=True)
    manual_input_ids = fields.One2many("project.key.result.manual.input",
                                       "key_result_id", "Manual inputs",
                                       copy=False)
    model_id = fields.Many2one('ir.model', string='Related Document Model',
                               domain=[('transient', '=', False)])
    automatic_model = fields.Char(related='model_id.model', readonly=True)
    automatic_domain = fields.Text("Automatic search domain",
                                   help="Can use 'task' in the domain "
                                        "referring to key result task as obj.")
    automatic_field = fields.Char("Field to Sum")
    follow_type_id = fields.Many2one("project.follow.type", "Follow type")
    result = fields.Float(digits=(16, 2), readonly=True, compute="_get_result")
    progress = fields.Float("Progress", compute="_get_result", digits=(16, 2))
    failed = fields.Boolean(compute="_get_result")
    active = fields.Boolean(default=True)
    compute = fields.Selection([('sum', 'Sum'), ('avg', 'Avg'),
                                ('count', 'Count')], "Calculation",
                               default="sum", required=True)


class ProjectKeyResultManualInput(models.Model):

    _name = "project.key.result.manual.input"
    _order = "create_date desc"

    name = fields.Char("Motivation", required=True)
    value = fields.Float(digits=(16, 2), required=True)
    key_result_id = fields.Many2one("project.key.result", "Key Result",
                                    ondelete="cascade")
    create_date = fields.Datetime('Created', readonly=True)
    create_uid = fields.Many2one('res.users', string='Creator', readonly=True)
