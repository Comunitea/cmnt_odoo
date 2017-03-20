# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class HrEmployeeRfidKey(models.Model):

    _name = "hr.employee.rfid.key"
    _rec_name = "cardId"

    cardId = fields.Char("Card Id", required=True)
    employee_id = fields.Many2one("hr.employee", "Employee", required=True)
    active = fields.Boolean("Active", default=True)
    description = fields.Text("Description")


class HrEmployeeRfidKeyLog(models.Model):

    _name = "hr.employee.rfid.key.log"
    _rec_name = "description"

    description = fields.Char("Message", required=True)
    employee_id = fields.Many2one("hr.employee", "Employee")
    create_date = fields.Datetime("Create date", readonly=True)


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    rfid_card_ids = fields.One2many("hr.employee.rfid.key", "employee_id",
                                    "RFID cards")
