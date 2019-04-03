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

from openerp import http
import json


class BaseNetelipPhoneController(http.Controller):

    @http.route('/netelip/calls', type='json', auth='none')
    def receive_calls(self, req):
        origin_phone = req.jsonrequest.get('src')
        dest_phone = req.jsonrequest.get('dst')
        userfield = req.jsonrequest.get('userfield')
        dtmf = req.jsonrequest.get('dtmf')
        call_id = req.jsonrequest.get('ID')
        api = req.jsonrequest.get('api')
        command = req.jsonrequest.get('command')
        options = req.jsonrequest.get('options')
        state = req.jsonrequest.get('status')
        description = req.jsonrequest.get('description')
        start_date = req.jsonrequest.get('startcall')
        call_duration = req.jsonrequest.get('durationcall')
        call_answered_duration = req.jsonrequest.get('durationcallanswered')
        partner_obj = http.request.registry['res.partner']
        partner_ids = partner_obj.search(['|', ('phone', '=', origin_phone),
                                          ('mobile', '=', origin_phone)],
                                         limit=1)
        if origin_phone and dest_phone and call_id:
            if not userfield:
                command = "record"
                options = "''"
                userfield = 1
            elif userfield in (1, 2):
                if partner_ids and userfield != 2:
                    user_data = http.request.registry['res.users'].\
                        search_read([('context_incall_popup', '=', True)],
                                    ['login'])
                    logins = [x['login'] for x in user_data]
                    caller_id = partner_obj.\
                        incall_notify_by_login(origin_phone, logins)
                    partner = partner_obj.browse(caller_id)
                    command = "callerid"
                    options = partner.name + ";" + origin_phone
                    userfield = 2
                else:
                    phonecall_obj = http.request.registry['crm.phonecall']
                    phonecall_id = phonecall_obj.\
                        create({'date': start_date,
                                'name': call_id,
                                'partner_phone': origin_phone,
                                'partner_id':
                                partner_ids and partner_ids[0] or False})
                    command = "ivr"
                    options = "General"
                    userfield = phonecall_id
            else:
                command = "ivr"
                options = "General"
            return json.dumps({'command': command,
                               'options': options,
                               'userfield': userfield})

    @http.route('/netelip/endcalls', type='json', auth='none')
    def finalize_calls(self, req):
        origin_phone = req.jsonrequest.get('src')
        dest_phone = req.jsonrequest.get('dst')
        userfield = req.jsonrequest.get('userfield')
        dtmf = req.jsonrequest.get('dtmf')
        call_id = req.jsonrequest.get('ID')
        api = req.jsonrequest.get('api')
        command = req.jsonrequest.get('command')
        options = req.jsonrequest.get('options')
        state = req.jsonrequest.get('status')
        description = req.jsonrequest.get('description')
        start_date = req.jsonrequest.get('startcall')
        call_duration = req.jsonrequest.get('durationcall')
        call_answered_duration = req.jsonrequest.get('durationcallanswered')
        if userfield:
            phonecall_obj = http.request.registry['crm.phonecall']
            phonecall = phonecall_obj.browse(userfield)
            phonecall.write({'description': description,
                             'state': 'done',
                             'duration': call_answered_duration})

    @http.route('/netelip/reportcalls', type='json', auth='none')
    def report_calls(self, req):
        print "REQ: ", req.jsonrequest
