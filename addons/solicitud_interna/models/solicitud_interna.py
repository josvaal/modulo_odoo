from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import re

class SolicitudInterna(models.Model):
    _name = 'solicitud.interna'
    _description = 'Sistema de Tickets - Solicitud Interna'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_solicitud desc, prioridad_nivel desc'
    _rec_name = 'numero_ticket'

    # Campos básicos
    numero_ticket = fields.Char(string='Número de Ticket', required=True, copy=False, readonly=True, default='Nuevo')
    name = fields.Char(string='Título', required=True, tracking=True)
    description = fields.Html(string='Descripción', tracking=True)
    
    # Categorización
    category = fields.Selection([
        ('material', 'Material de Oficina'),
        ('soporte', 'Soporte Técnico'),
        ('mantenimiento', 'Mantenimiento'),
        ('permisos', 'Permisos'),
        ('rrhh', 'Recursos Humanos'),
        ('finanzas', 'Finanzas'),
        ('it', 'Tecnología'),
        ('otros', 'Otros'),
    ], string='Categoría', required=True, tracking=True)
    
    subcategory = fields.Char(string='Subcategoría', tracking=True)
    
    # Estados del ticket
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('en_proceso', 'En Proceso'),
        ('esperando_respuesta', 'Esperando Respuesta'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True, required=True)
    
    # Fechas importantes
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now, tracking=True, readonly=True)
    fecha_asignacion = fields.Datetime(string='Fecha de Asignación', tracking=True, readonly=True)
    fecha_inicio = fields.Datetime(string='Fecha de Inicio', tracking=True)
    fecha_limite = fields.Datetime(string='Fecha Límite', tracking=True)
    fecha_resolucion = fields.Datetime(string='Fecha de Resolución', tracking=True, readonly=True)
    fecha_cierre = fields.Datetime(string='Fecha de Cierre', tracking=True, readonly=True)
    
    # Usuarios involucrados
    solicitante_id = fields.Many2one('res.users', string='Solicitante', default=lambda self: self.env.user, tracking=True, required=True)
    gestor_id = fields.Many2one('res.users', string='Gestor Asignado', tracking=True)
    supervisor_id = fields.Many2one('res.users', string='Supervisor', tracking=True)
    
    # Información adicional
    departamento_id = fields.Many2one('departamento.solicitud', string='Departamento', required=True)
    tipo_material_id = fields.Many2one('tipo.material', string='Tipo de Material')
    prioridad_id = fields.Many2one('prioridad.solicitud', string='Prioridad', required=True)
    proveedor_id = fields.Many2one('proveedor.servicio', string='Proveedor de Servicio')
    
    # Campos calculados
    prioridad_nivel = fields.Integer(related='prioridad_id.nivel', store=True)
    tiempo_resolucion = fields.Float(string='Tiempo de Resolución (horas)', compute='_compute_tiempo_resolucion', store=True)
    dias_pendiente = fields.Integer(string='Días Pendiente', compute='_compute_dias_pendiente')
    esta_vencido = fields.Boolean(string='Está Vencido', compute='_compute_esta_vencido', search='_search_esta_vencido')
    
    # Campos de seguimiento
    comentarios = fields.Text(string='Comentarios Internos')
    solucion = fields.Html(string='Solución Aplicada')
    costo_estimado = fields.Float(string='Costo Estimado')
    costo_real = fields.Float(string='Costo Real')
    
    # Relaciones
    historial_estado_ids = fields.One2many('historial.estado.solicitud', 'solicitud_id', string='Historial de Estados')
    comentario_ids = fields.One2many('comentario.solicitud', 'solicitud_id', string='Comentarios')
    encuesta_ids = fields.One2many('encuesta.satisfaccion', 'solicitud_id', string='Encuestas de Satisfacción')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'solicitud.interna')], string='Adjuntos')
    
    # Campos de satisfacción
    puntuacion_satisfaccion = fields.Selection([
        ('1', 'Muy Insatisfecho'),
        ('2', 'Insatisfecho'),
        ('3', 'Neutral'),
        ('4', 'Satisfecho'),
        ('5', 'Muy Satisfecho'),
    ], string='Puntuación de Satisfacción')
    
    # Campos de color para kanban
    color = fields.Integer(string='Color', compute='_compute_color')
    
    @api.model
    def create(self, vals):
        if vals.get('numero_ticket', 'Nuevo') == 'Nuevo':
            vals['numero_ticket'] = self.env['ir.sequence'].next_by_code('solicitud.interna') or 'Nuevo'
        if 'state' not in vals:
            vals['state'] = 'pendiente'
        return super(SolicitudInterna, self).create(vals)
    
    @api.depends('fecha_solicitud', 'fecha_resolucion')
    def _compute_tiempo_resolucion(self):
        for record in self:
            if record.fecha_solicitud and record.fecha_resolucion:
                delta = record.fecha_resolucion - record.fecha_solicitud
                record.tiempo_resolucion = delta.total_seconds() / 3600
            else:
                record.tiempo_resolucion = 0
    
    @api.depends('fecha_solicitud')
    def _compute_dias_pendiente(self):
        for record in self:
            if record.fecha_solicitud and record.state not in ['cerrado', 'cancelado']:
                delta = fields.Datetime.now() - record.fecha_solicitud
                record.dias_pendiente = delta.days
            else:
                record.dias_pendiente = 0
    
    @api.depends('fecha_limite', 'state')
    def _compute_esta_vencido(self):
        for record in self:
            if record.fecha_limite and record.state not in ['cerrado', 'cancelado', 'resuelto']:
                record.esta_vencido = fields.Datetime.now() > record.fecha_limite
            else:
                record.esta_vencido = False

    def _search_esta_vencido(self, operator, value):
        if operator not in ('=', '!=') or not isinstance(value, bool):
            raise UserError(_("Operation not supported"))
        now = fields.Datetime.now()
        closed_states = ['cerrado', 'cancelado', 'resuelto']
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('fecha_limite', '!=', False), ('fecha_limite', '<', now), ('state', 'not in', closed_states)]
        else:
            return ['|', '|', ('fecha_limite', '=', False), ('fecha_limite', '>=', now), ('state', 'in', closed_states)]
    
    @api.depends('prioridad_id', 'state', 'esta_vencido')
    def _compute_color(self):
        for record in self:
            if record.esta_vencido:
                record.color = 1  # Rojo
            elif record.prioridad_id.nivel >= 4:
                record.color = 3  # Amarillo
            elif record.state == 'resuelto':
                record.color = 10  # Verde
            else:
                record.color = 0  # Sin color
    
    @api.constrains('fecha_limite')
    def _check_fecha_limite(self):
        for record in self:
            if record.fecha_limite and record.fecha_limite < record.fecha_solicitud:
                raise ValidationError('La fecha límite no puede ser anterior a la fecha de solicitud.')
    
    def _crear_historial_estado(self, estado_anterior, estado_nuevo):
        self.env['historial.estado.solicitud'].create({
            'solicitud_id': self.id,
            'estado_anterior': estado_anterior,
            'estado_nuevo': estado_nuevo,
            'usuario_id': self.env.user.id,
        })
    
    def action_enviar(self):
        if self.state == 'borrador':
            estado_anterior = self.state
            self.state = 'pendiente'
            self._crear_historial_estado(estado_anterior, self.state)
            self.message_post(body='Ticket enviado para revisión.')
    
    def action_asignar(self):
        if not self.gestor_id:
            raise UserError('Debe asignar un gestor antes de cambiar el estado.')
        estado_anterior = self.state
        self.state = 'asignado'
        self.fecha_asignacion = fields.Datetime.now()
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body=f'Ticket asignado a {self.gestor_id.name}.')
    
    def action_en_proceso(self):
        estado_anterior = self.state
        self.state = 'en_proceso'
        if not self.fecha_inicio:
            self.fecha_inicio = fields.Datetime.now()
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body='Ticket en proceso de resolución.')
    
    def action_esperando_respuesta(self):
        estado_anterior = self.state
        self.state = 'esperando_respuesta'
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body='Ticket en espera de respuesta del solicitante.')
    
    def action_resolver(self):
        if not self.solucion:
            raise UserError('Debe proporcionar una solución antes de resolver el ticket.')
        estado_anterior = self.state
        self.state = 'resuelto'
        self.fecha_resolucion = fields.Datetime.now()
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body='Ticket resuelto.')
    
    def action_cerrar(self):
        estado_anterior = self.state
        self.state = 'cerrado'
        self.fecha_cierre = fields.Datetime.now()
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body='Ticket cerrado.')
    
    def action_cancelar(self):
        estado_anterior = self.state
        self.state = 'cancelado'
        self._crear_historial_estado(estado_anterior, self.state)
        self.message_post(body='Ticket cancelado.')
    
    def action_reabrir(self):
        if self.state in ['cerrado', 'cancelado']:
            estado_anterior = self.state
            self.state = 'pendiente'
            self._crear_historial_estado(estado_anterior, self.state)
            self.message_post(body='Ticket reabierto.')
    
    @api.model
    def enviar_recordatorios_vencimiento(self):
        """Método para enviar recordatorios de tickets próximos a vencer"""
        fecha_limite = fields.Datetime.now() + timedelta(days=1)
        tickets_proximos = self.search([
            ('fecha_limite', '<=', fecha_limite),
            ('state', 'not in', ['cerrado', 'cancelado', 'resuelto'])
        ])
        
        for ticket in tickets_proximos:
            if ticket.gestor_id:
                ticket.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=ticket.gestor_id.id,
                    summary=f'Ticket {ticket.numero_ticket} próximo a vencer',
                    note=f'El ticket "{ticket.name}" vence el {ticket.fecha_limite}'
                )
