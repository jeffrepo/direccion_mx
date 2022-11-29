# -*- encoding: utf-8 -*-

from lxml import etree

from odoo import models, fields, api


class partner(models.Model):

    _inherit = 'res.partner'
    
       
    colonia_id = fields.Many2one('res.country.state.municipio.colonia', string="Colonia", tracking=True)
    municipio_id = fields.Many2one('res.country.state.municipio', string='Municipio', tracking=True)
    ciudad_id = fields.Many2one('res.country.state.ciudad', string='Ciudad', tracking=True)
    city = fields.Char(related='ciudad_id.name',readonly=True)
    l10n_mx_edi_colony = fields.Char(related='colonia_id.name',readonly=True)


    @api.model
    def _fields_view_get_address(self, arch):
        arch = super(partner, self)._fields_view_get_address(arch)
        # render the partner address accordingly to address_view_id
        doc = etree.fromstring(arch)
        for city_node in doc.xpath("//field[@name='city']"):
            replacement_xml = """
            <div>
                <field name="country_enforce_cities" invisible="1"/>
                <field name='city' invisible="1"/>
                <field name='city_id' invisible="1"/>
            </div>
            """
            city_id_node = etree.fromstring(replacement_xml)
            city_node.getparent().replace(city_node, city_id_node)

        for city_id_node in doc.xpath("//field[@name='city_id']"):
            replacement_xml = """
            <div>
                <field name="country_enforce_cities" invisible="1"/>
                <field name='city' invisible="1"/>
                <field name='city_id' invisible="1"/>
            </div>
            """
            replacement_node = etree.fromstring(replacement_xml)
            city_id_node.getparent().replace(city_id_node, replacement_node)

        arch = etree.tostring(doc, encoding='unicode')
        return arch



    @api.onchange('city_id')
    def _onchange_city_id(self):
        #self.city = self.city_id.name
        #self.zip = self.city_id.zipcode
        #self.state_id = self.city_id.state_id
        return



    @api.depends('municipio_id','municipio_id.ciudad_id','município_id.state_id')
    def update_ciudad_id_state_id(self):
        self.ciudad_id = self.municipio_id.ciudad_id
        self.state_id = self.municipio_id.state_id
        return
   
    @api.depends('ciudad_id','cuidad_id.name')
    def update_city(self):
        self.city=self.ciudad_id and self.ciudad_id.name or ''
        return

    @api.depends('colonia_id')
    def update_l10n_mx_edi_colony(self):
        self.l10n_mx_edi_colony=self.colonia_id and self.colonia_id.name or ''
        return



    @api.onchange('ciudad_id')
    def onchange_ciudad(self):
        if self.ciudad_id and not self.colonia_id:
            self.municipio_id=self.ciudad_id.municipio_ids.ids[0]
        return 

    @api.onchange('municipio_id')
    def onchange_municipio(self):
        if self.municipio_id:
            self.state_id =self.municipio_id.state_id
            return {
                'value':{
                    'ciudad_id': self.municipio_id.ciudad_id.id or False,
                    'state_id': self.state_id.id,
                    'country_id': self.state_id.country_id.id, 
                }
            }
        return {}
    @api.onchange('colonia_id')
    def onchange_colonia(self):
        if self.colonia_id:
            self.municipio_id = self.colonia_id.municipio_id
            return {
                'value':{
                    'zip': self.colonia_id.cp,
                    'municipio_id': self.colonia_id.municipio_id.id,
                    'ciudad_id': self.colonia_id.municipio_id.ciudad_id.id or False, 
                    'state_id': self.colonia_id.municipio_id.state_id.id,
                    'country_id': self.colonia_id.municipio_id.state_id.country_id.id, 
                }
            }
        return {}
    
