{
    'name': 'Sistema de Tickets - Solicitudes Internas',
    'version': '2.0.0',
    'summary': 'Sistema robusto de gestión de tickets y solicitudes internas',
    'description': '''
        Sistema completo de gestión de tickets para solicitudes internas
        ================================================================
        
        Características principales:
        * Gestión completa de tickets con estados avanzados
        * Sistema de prioridades y categorías
        * Seguimiento de tiempos y métricas
        * Historial completo de cambios
        * Sistema de comentarios y adjuntos
        * Encuestas de satisfacción
        * Plantillas de solicitudes
        * Gestión de departamentos y proveedores
        * Reportes y análisis avanzados
        * Notificaciones automáticas
        * Múltiples vistas: Kanban, Lista, Calendario, Gráficos
        
        Roles de usuario:
        * Solicitante: Puede crear y seguir sus tickets
        * Gestor: Puede gestionar todos los tickets y configuraciones
        * Administrador: Acceso completo al sistema
    ''',
    'author': 'Sistema de Tickets',
    'website': 'https://www.tuempresa.com',
    'category': 'Services/Helpdesk',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'portal',
    ],
    'data': [
        # Seguridad
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Datos iniciales
        'data/ir_sequence_data.xml',
        'data/prioridad_data.xml',
        'data/departamento_data.xml',
        
        # Vistas principales
        'views/solicitud_interna_views.xml',
        'views/tablas_extra_views.xml',
        'views/solicitud_interna_menu.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
    'external_dependencies': {
        'python': [],
    },
}
