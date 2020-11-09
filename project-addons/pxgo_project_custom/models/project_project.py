# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    sale_id = fields.Many2one("sale.order", "Sale Order")

