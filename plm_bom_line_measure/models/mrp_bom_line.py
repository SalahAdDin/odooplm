"""
Created on 19/09/2018
@author: salahaddin
"""

from odoo import models
from odoo import fields
from odoo import _


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    measure = fields.Char(_('Measure'))
    measure_uom_id = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the products measure")
