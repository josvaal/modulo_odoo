{
    'name': 'solicitud_interna',
    'version': '18.0.1.0',
    'summary': 'Sistema de Gestión de Solicitudes Internas',
    'category': 'Tools',
    'author': 'Tu Empresa',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/solicitud_interna_views.xml',
        'views/solicitud_interna_menu.xml'
    ],
    'application': True,
    'installable': True
}
