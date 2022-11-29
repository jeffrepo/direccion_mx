# -*- coding: utf-8 -*-

import odoo
from odoo import api, fields, models, _
import re


class CodigoPostal(models.Model):
    _name = "res.country.state.cp"

    name = fields.Char("Codigo Postal", size=128)
    state_id = fields.Many2one('res.country.state', string='Estado')
    ciudad_id = fields.Many2one('res.country.state.ciudad', string='Localidad')
    municipio_id = fields.Many2one('res.country.state.municipio', string='Municipio')

class Ciudad(models.Model):
    _name = 'res.country.state.ciudad'
    
    state_id = fields.Many2one('res.country.state', string='Estado', required=True)
    municipio_ids = fields.One2many('res.country.state.municipio','ciudad_id',string='Municipios')
    name = fields.Char(string='Name', size=256, required=True)
    clave_sat = fields.Char("Clave SAT")


class Municipio(models.Model):
    _name = 'res.country.state.municipio'
    
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    ciudad_id = fields.Many2one('res.country.state.ciudad', string='City')
    name = fields.Char(string='Name', size=64, required=True)
    clave_sat = fields.Char(string="Clave SAT")

    @api.depends('ciudad_id','ciudad_id.state_id')
    def update_state_id(self):
        self.state_id = self.ciudad_id.state_id
        return
 

class Colonia(models.Model):
    _name = 'res.country.state.municipio.colonia'
    
    municipio_id = fields.Many2one('res.country.state.municipio', 
        string='Municipio', required=True)
    name = fields.Char(string='Name', size=256, required=True)
    cp = fields.Char(string='Código Postal', size=10)
    clave_sat = fields.Char("Clave SAT")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if re.match("^\d{4,5}$", name):
            recs = self.search([('cp', 'ilike', name)] + args,  limit=limit)
            res=recs.name_get()
            #sorted(locations, key=lambda (id, name): ids.ids.index(id))
            return res
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
