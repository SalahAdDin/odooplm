##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2010 OmniaSolutions (<http://omniasolutions.eu>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
Created on 30 Aug 2016

@author: Daniel Smerghetto
"""

from odoo import _
from odoo import api
from odoo import fields
from odoo import models

from odoo.addons.plm.models.product_product import USED_STATES

USED_STATES.append(('suspended', _('Suspended')))

USE_DIC_STATES = dict(USED_STATES)


class PlmComponentExtension(models.Model):
    _inherit = 'product.product'

    state = fields.Selection(
        USED_STATES,
        _('Status'),
        help=_("The status of the product."),
        readonly="True",
        default='draft',
        required=True
    )
    old_state = fields.Char(
        size=128,
        name=_("Old Status")
    )

    @property
    def actions(self):
        action_dict = super(PlmComponentExtension, self).actions
        action_dict['suspended'] = self.action_suspend
        return action_dict

    @api.multi
    def action_suspend(self):
        """
            reactivate the object
        """
        defaults = {'old_state': self.state, 'state': 'suspended'}
        obj_id = self.write(defaults)
        if obj_id:
            self.wf_message_post(body=_('Status moved to:{}.'.format(USE_DIC_STATES[defaults['state']])))
        return obj_id

    @api.multi
    def action_unsuspend(self):
        """
            reactivate the object
        """
        defaults = {'old_state': self.state, 'state': 'draft'}
        obj_id = self.write(defaults)
        if obj_id:
            self.wf_message_post(body=_('Status moved to:{}.'.format(USE_DIC_STATES[defaults['state']])))
        return obj_id
