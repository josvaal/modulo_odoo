from odoo import models, fields, api

class SolicitudInterna(models.Model):
    _name = 'solicitud.interna'
    _description = 'Solicitud Interna'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Título', required=True, tracking=True)
    description = fields.Text(string='Descripción', tracking=True)
    category = fields.Selection([
        ('material', 'Material de Oficina'),
        ('soporte', 'Soporte Técnico'),
        ('mantenimiento', 'Mantenimiento'),
        ('permisos', 'Permisos'),
        ('otros', 'Otros'),
    ], string='Categoría', required=True, tracking=True)
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    ], string='Estado', default='pendiente', tracking=True)
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now, tracking=True)
    solicitante_id = fields.Many2one('res.users', string='Solicitante', default=lambda self: self.env.user, tracking=True)
    gestor_id = fields.Many2one('res.users', string='Gestor', tracking=True)
    comentarios = fields.Text(string='Comentarios')
    departamento_id = fields.Many2one('departamento.solicitud', string='Departamento')
    tipo_material_id = fields.Many2one('tipo.material', string='Tipo de Material')
    prioridad_id = fields.Many2one('prioridad.solicitud', string='Prioridad')
    proveedor_id = fields.Many2one('proveedor.servicio', string='Proveedor de Servicio')
    historial_estado_ids = fields.One2many('historial.estado.solicitud', 'solicitud_id', string='Historial de Estados')
    comentario_ids = fields.One2many('comentario.solicitud', 'solicitud_id', string='Comentarios')
    encuesta_ids = fields.One2many('encuesta.satisfaccion', 'solicitud_id', string='Encuestas de Satisfacción')

    def action_en_proceso(self):
        self.state = 'en_proceso'

    def action_completada(self):
        self.state = 'completada'
