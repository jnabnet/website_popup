# -*- coding: utf-8 -*-
import werkzeug
import json
import base64

import openerp.http as http
from openerp.http import request

from openerp.addons.website.models.website import slug

class PopupCampaign(http.Controller):

    @http.route('/popup/campaign',type="http", auth="public", csrf=False)
    def my_insert_campaign_popup(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        ref_url = ""
        if 'Referer' in http.request.httprequest.headers:
            ref_url = http.request.httprequest.headers['Referer']

        return_url = ref_url
        if 'return_url' in values:
            return_url = values['return_url']

        new_partner = request.env['res.partner'].sudo().create({'name': values['name'], 'email': values['email']})
        
        form_campaign = request.env['marketing.campaign'].sudo().browse(int(values['popup_campaign_id']))

        #Add the new partner to a campaign
        for act in form_campaign.activity_ids:
            if act.start:
                wi = request.env['marketing.campaign.workitem'].sudo().create({'campaign_id': form_campaign.id, 'activity_id': act.id, 'partner_id': new_partner.id, 'res_id': new_partner.id})
                wi.process()

        return werkzeug.utils.redirect(return_url)