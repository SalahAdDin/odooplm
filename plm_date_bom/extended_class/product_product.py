# -*- encoding: utf-8 -*-
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

from odoo import models
from odoo import api


class ProductExtension(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

#     @api.model
#     def updateObsoleteLevel(self, prodBrws, obsolete_recursive=False):
#         envObj = self.env['mrp.bom.line']
#         bomLines = envObj.search([(
#             'product_id', '=', prodBrws.id
#             )])
#         bomList = []
#         for bomLineBrws in bomLines:
#             bomList.append(bomLineBrws.bom_id)
#         bomList = list(set(bomList))
#         for bomBrws in bomList:
#             bomBrws.obsolete_presents = True
#             bomBrws.obsolete_presents_recursive = bomBrws.obsolete_presents
    
    @api.model
    def updateObsoleteRecursive(self, prodBrws):
        bomTmpl = self.env['mrp.bom']
        struct = prodBrws.getParentBomStructure()
        
        def recursion(struct2, isRoot=False):
            for vals, parentsList in struct2:
                bom_id = vals.get('bom_id', False)
                if bom_id:
                    bomBrws = bomTmpl.browse(bom_id)
                    bomBrws._obsolete_compute()
                    if not isRoot:
                        bomBrws.obsolete_presents_recursive = True
                recursion(parentsList)
            
        recursion(struct, isRoot=True)

    @api.multi
    def write(self, vals):
        res = super(ProductExtension, self).write(vals)
        statePresent = vals.get('state', None)
        if statePresent == 'obsoleted':
            # Here I force compute obsolete presents flag in all boms
            for prodTmplBrws in self:
                for prodBrws in prodTmplBrws.product_variant_ids:
                    self.updateObsoleteRecursive(prodBrws)
        return res

