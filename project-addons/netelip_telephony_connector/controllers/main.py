# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019 Comunitea All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from odoo import http, fields
import json
import pytz
import webdav.client as wc
import base64
import os


class BaseNetelipPhoneController(http.Controller):

    @http.route('/netelip/calls', type='http', auth='none', csrf=False)
    def receive_calls(self, **req):
        origin_phone = req.get('src')
        dest_phone = req.get('dst')
        userfield = req.get('userfield')
        call_id = req.get('ID')
        typesrc = req.get('typesrc')
        command = req.get('command')
        options = req.get('options')
        state = req.get('statuscall') or req.get('status')
        description = req.get('description')
        start_date = req.get('startcall')
        call_answered_duration = req.get('durationcallanswered')
        if origin_phone and dest_phone and call_id and typesrc == 'did':
            if not userfield and state != 'OK' and \
                    (len(dest_phone) > 4 or len(origin_phone) > 4):
                command = "record"
                options = "''"
                userfield = "M1"
            elif userfield == "M1":
                command = "callerid"
                company_obj = http.request.env['res.company']
                company = company_obj.sudo().\
                    search([('netelip_phone', '!=', False)], limit=1)
                partner_obj = http.request.env['res.partner']
                partners_data = partner_obj.sudo().\
                    get_record_from_phone_number(origin_phone)
                if company and partners_data:
                    partner_name = partners_data[2]
                    partner_name = ''.join([i if ord(i) < 128 else ' ' for i
                                            in partner_name])
                    options = partner_name + u" " + origin_phone + \
                        u";" + company.netelip_phone
                elif company:
                    options = origin_phone + u" Unknown;" + \
                        company.netelip_phone
                else:
                    options = "''"
                userfield = "C1"
            elif userfield == "C1" and state != 'CANCEL':
                phone = origin_phone
                command = "queue"
                options = "general"
                partner_obj = http.request.env['res.partner']
                partners_data = partner_obj.sudo().\
                    get_record_from_phone_number(phone)
                phonecall_obj = http.request.env['crm.phonecall'].sudo()
                phonecall_id = phonecall_obj.\
                    create({'date': fields.Datetime.
                            to_string(pytz.timezone(phonecall_obj.env.user.tz).
                                      localize(fields.Datetime.
                                               from_string(start_date)).
                                      astimezone(pytz.utc)),
                            'name': call_id,
                            'partner_phone': phone,
                            'direction': 'inbound',
                            'categ_id':
                            phonecall_obj.env.ref('crm.categ_phone2').id,
                            'partner_id':
                            partners_data and partners_data[1] or False})
                user = http.request.env['res.users'].sudo().\
                    search([('netelip_ext', '=', origin_phone)], limit=1)
                if user:
                    phonecall_id.user_id = user.id
                userfield = phonecall_id.id
            elif userfield != 'C2':
                phonecall_obj = http.request.env['crm.phonecall'].sudo()
                phonecall = phonecall_obj.search([('name', '=', call_id)],
                                                 limit=1)
                if phonecall:
                    vals = {'description': description}
                    if call_answered_duration:
                        vals['duration'] = float(call_answered_duration)/100.0
                    phonecall.write(vals)
                command = "hangup"
                options = "''"
            if command:
                return json.dumps({'command': command,
                                   'options': options,
                                   'userfield': userfield})

    @http.route('/netelip/new_call', type='http', auth='none')
    def make_calls(self, **req):
        pass

    @http.route('/netelip/reportcalls', type='http', auth='none', csrf=False)
    def report_calls(self, **req):
        calls = req.get('calls')
        phonecall_obj = http.request.env['crm.phonecall'].sudo()
        user_obj = http.request.env['res.users'].sudo()
        options = {
            'webdav_hostname':
            user_obj.env.user.company_id.netelip_webdav_hostname,
            'webdav_login': user_obj.env.user.company_id.netelip_webdav_login,
            'webdav_password':
            user_obj.env.user.company_id.netelip_webdav_password,
            'webdav_root': "/remote.php/webdav"
        }
        client = wc.Client(options)
        for call_data in json.loads(calls):
            call_id = call_data['ID']
            description = call_data["dstname"]
            call = phonecall_obj.search([('name', '=', call_id)], limit=1)
            if call:
                info = description
                if 'Ext' in info:
                    if 'APIVoice' in call.description:
                        if client.check(call.description):
                            fname = u'/tmp/' + call.description.split('/')[-1]
                            client.download(call.description, fname)
                            f = open(fname, 'r')
                            encoded_string = base64.b64encode(f.read())
                            os.remove(fname)
                            fname = fname.split('/')[-1]
                            http.request.env['ir.attachment'].sudo().\
                                create({'name': fname,
                                        'res_name': call.name,
                                        'res_model': 'crm.phonecall',
                                        'res_id': call.id,
                                        'datas': encoded_string,
                                        'datas_fname': fname})
                            client.clean(call.description)
                    extension = info.split(' ')[-1]
                    user = user_obj.search([('netelip_ext', '=', extension)],
                                           limit=1)
                    if user:
                        call.write({'user_id': user.id,
                                    'state': 'done',
                                    'description':
                                    call.description + u'\n' + description})
                else:
                    call.write({'state': 'cancel',
                                'description':
                                call.description + u'\n' + description})
