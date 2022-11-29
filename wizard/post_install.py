# -*- encoding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
import logging
import os
import inspect
import csv

_logger= logging.getLogger(__name__)


class direccion_upload_address_wizard(models.TransientModel):

    _name = 'direccion_mx.postinstall'
    _inherit = 'res.config.settings' 
    
    colonias = fields.Boolean("Inicializar tablas de colonias, municipios y ciudades") 
    actualizar = fields.Boolean("Eliminar datos al actualizar el modulo.(Solo Aplica para registros nuevos)") 

    def set_values(self):
        if self.colonias:
            ciudades_obj=self.env['res.country.state.ciudad']
            colonias_obj=self.env['res.country.state.municipio.colonia']
            municipios_obj=self.env['res.country.state.municipio']
            current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            fname_model =  current_path+"/../data/res.country.state.ciudad.csv"
            import_fields = []
            values = []
            if self.actualizar :
                ciudades_obj=ciudades_obj.with_context(module='direccion_mx')
                colonias_obj=colonias_obj.with_context(module='direccion_mx')
                municipios_obj=municipios_obj.with_context(module='direccion_mx')
            else:
                ciudades_obj=ciudades_obj.with_context(module='direccion_mx', noupdate=True)
                colonias_obj=colonias_obj.with_context(module='direccion_mx', noupdate=True)
                municipios_obj=municipios_obj.with_context(module='direccion_mx',noupdate=True)
            with open(fname_model, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                indx = 0
                for row in spamreader:
                    if indx == 0:
                        import_fields = row
                    else:
                        row[1]=row[1].encode('utf-8')
                        res=self.env['ir.model.data'].get_object_reference('base',row[2].split('.')[1])
                        row[2]=res[1]
                        res=ciudades_obj.load(import_fields, [row])
                        _logger.info('Agregando ciudad %s - %s' % (indx, row[1]))
                    indx += 1
            fname_model =  current_path+"/../data/res.country.state.municipio.csv"
            import_fields = []
            values = []
            self._cr.commit()
            _logger.info('Agregando municipios...........................................................')
            with open(fname_model, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                indx = 0
                for row in spamreader:
                    if indx == 0:
                        import_fields = row
                    else:
                        row[1]=row[1].encode('utf-8')
                        res=self.env['ir.model.data'].get_object_reference('base',row[2].split('.')[1])
                        row[2]=res[1]
                        if row[3] != '' :
                            res=self.env['ir.model.data'].get_object_reference('direccion_mx',row[3])
                            row[3]=res[1]
                        res=municipios_obj.load(import_fields, [row])
                        _logger.info('Agregando municipio %s - %s' % (indx, row[1]))
                    indx += 1
            fname_model =  current_path+"/../data/res.country.state.municipio.colonia.csv"
            import_fields = []
            values = []
            self._cr.commit()
            _logger.info('Agregando colonias............................................................')
            with open(fname_model, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                indx = 0
                for row in spamreader:
                    if indx == 0:
                        import_fields = row
                    else:
                        row[1]=row[1].encode('utf-8')
                        if row[3] != '' :
                            res=self.env['ir.model.data'].get_object_reference('direccion_mx',row[3])
                            row[3]=res[1]
                        res=colonias_obj.load(import_fields, [row])
                        _logger.info('Agregando colonia %s - %s' % (indx, row[1]))
                        if not indx%5000 :
                            self._cr.commit()
                            _logger.info('.............................................................Commit................................................')
                    indx += 1
            _logger.info('Inicializacion Terminada')
        return True

