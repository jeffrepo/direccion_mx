# -*- encoding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
import time
import base64
from pylev3 import Levenshtein
class direccion_upload_address_wizard(models.TransientModel):

    _name = 'direccion_mx.wizard'
    
    
    datos = fields.Binary('Data File', required=True)
    error_tolerant = fields.Boolean(_("Ignorar registros con C.P. inválido")) 
    
    def _score(self, word, word2):
        word = word.strip().lower()
        word2 = word2.strip().lower()
        distancia = []
        if not ' ' in word and ' ' in word2:
            for part in word2.split(' '):
                distancia.append(Levenshtein.wf(word, part))
        else:        
            distancia.append(Levenshtein.wf(word, word2))
        return min(distancia)

    def action_process(self):
        data = base64.decodestring(self.datos)
        partner_obj = self.env['res.partner']
        model_data_obj = self.env['ir.model.data']
        colonia_obj = self.env['res.country.state.municipio.colonia']
        for line in data.decode('utf-8').split("\n"):
            line = line.replace("\n", "").replace("\r", "")
            if line != '':
                try:
                    external_id, cp, colonia_test = line.split(',')
                    split = external_id.split('.')
                except:
                     raise exceptions.except_orm(_('Error'), _('Formato erroneo en la linea ' + line))
                if not cp:
                    continue
                if len(split) == 2:
                    module = split[0]
                    external_id = split[1]
                else:
                    module = ''
                try:
                    partner = model_data_obj.get_object( module, external_id)
                except:
                   raise exceptions.except_orm(_('Error'),_( 'El ID esta mal en la linea ' + line + " (" + module + " " + external_id + ")"))
                if not partner:
                     raise exceptions.except_orm(_('Error'), _('El partner con id ' + module + '.' + external_id + " no existe"))
                colonia_ids = colonia_obj.search([('cp','=',cp)])
                if not colonia_ids:
                    if self.error_tolerant:
                        continue
                    else:
                        raise exceptions.except_orm(_('Error'), _('Ninguna colonia encontrada para cp ' + cp + ' en la linea ' + line))
                mejor_match = {'score':-1, 'model':None}
                for colonia in colonia_ids:
                    distancia = self._score(colonia_test, colonia.name)
                    if mejor_match['score'] == -1 or distancia < mejor_match['score']:
                        mejor_match['score'] = distancia
                        mejor_match['model'] = colonia
                colonia = mejor_match['model']
                municipio_id = colonia.municipio_id
                partner.write({
                    'colonia_id': colonia.id,
                    'zip': colonia.cp,
                    'municipio_id': municipio_id.id,
                    'ciudad_id': municipio_id.ciudad_id.id or False,
                    'state_id': municipio_id.state_id.id,
                    'country_id': municipio_id.state_id.country_id.id,
                })
        return True

        
