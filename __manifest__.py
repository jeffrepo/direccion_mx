# -*- coding: utf-8 -*-
{
    'name': "direccion_mx",

    'summary': """
         Direcciones que cumplen con los requerimientos del SAT""",

    'description': """
        Este modulo instala los municipios y colonias disponibles en el servicio postal mexicano 
        asegurando que los partners tendran una direccion valida.
        Al instalar o actualizar el módulo este muestra un wizard donde  se pueden inicializar los datos de ciudades municipios y colonias que ya trae el módulo.
        En el wizard aparecen dos opciones: inicializar las tablas de colonias, municipios y ciudades  que importa los datos del csv 
        y viene otra opcion que permite hacer que los datos importados se puedan borrar o no en las siguientes actualizaciones ( por default los datos no se pueden borrar).
    """,

    'author': "silvau",
    'website': "http://www.zeval.com.mx",
    'category': 'account',
    'version': '14.1',

    'depends': ['base_address_city','l10n_mx_edi','contacts'],

    'data': [
        #'data/res_country_state_ciudad.xml',
        #'data/res_country_state_municipio.xml',
        #'data/res_country_state_municipio_colonia.xml',
        'views/partner_view.xml',
        'views/res_country_view.xml',
        'wizard/upload_address.xml',
        'wizard/post_install.xml',
    ],
    'init_xml': [
        'security/ir.model.access.csv'
    ],

}
