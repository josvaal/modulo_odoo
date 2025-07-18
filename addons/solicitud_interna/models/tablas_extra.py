from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DepartamentoSolicitud(models.Model):
    _name = 'departamento.solicitud'
    _description = 'Departamento que puede hacer solicitudes'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    responsable_id = fields.Many2one('res.users', string='Responsable')
    supervisor_id = fields.Many2one('res.users', string='Supervisor')
    activo = fields.Boolean(string='Activo', default=True)
    descripcion = fields.Text(string='Descripción')
    ubicacion = fields.Char(string='Ubicación')
    presupuesto_anual = fields.Float(string='Presupuesto Anual')
    
    # Estadísticas
    total_solicitudes = fields.Integer(string='Total Solicitudes', compute='_compute_estadisticas')
    solicitudes_pendientes = fields.Integer(string='Solicitudes Pendientes', compute='_compute_estadisticas')
    
    @api.depends('name')
    def _compute_estadisticas(self):
        for record in self:
            solicitudes = self.env['solicitud.interna'].search([('departamento_id', '=', record.id)])
            record.total_solicitudes = len(solicitudes)
            record.solicitudes_pendientes = len(solicitudes.filtered(lambda s: s.state in ['pendiente', 'asignado', 'en_proceso']))
    
    @api.constrains('codigo')
    def _check_codigo_unico(self):
        for record in self:
            if self.search_count([('codigo', '=', record.codigo), ('id', '!=', record.id)]) > 0:
                raise ValidationError('El código del departamento debe ser único.')

class TipoMaterial(models.Model):
    _name = 'tipo.material'
    _description = 'Tipo de material de oficina'
    _order = 'categoria, name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    descripcion = fields.Text(string='Descripción')
    categoria = fields.Selection([
        ('papeleria', 'Papelería'),
        ('tecnologia', 'Tecnología'),
        ('mobiliario', 'Mobiliario'),
        ('limpieza', 'Limpieza'),
        ('otros', 'Otros'),
    ], string='Categoría', required=True)
    stock_actual = fields.Integer(string='Stock Actual', default=0)
    stock_minimo = fields.Integer(string='Stock Mínimo', default=5)
    precio_unitario = fields.Float(string='Precio Unitario')
    proveedor_id = fields.Many2one('proveedor.servicio', string='Proveedor Principal')
    activo = fields.Boolean(string='Activo', default=True)
    
    # Campo calculado para alertas
    necesita_reposicion = fields.Boolean(string='Necesita Reposición', compute='_compute_necesita_reposicion')
    
    @api.depends('stock_actual', 'stock_minimo')
    def _compute_necesita_reposicion(self):
        for record in self:
            record.necesita_reposicion = record.stock_actual <= record.stock_minimo

class HistorialEstadoSolicitud(models.Model):
    _name = 'historial.estado.solicitud'
    _description = 'Historial de cambios de estado de solicitudes'
    _order = 'fecha_cambio desc'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True, ondelete='cascade')
    estado_anterior = fields.Char(string='Estado Anterior')
    estado_nuevo = fields.Char(string='Estado Nuevo', required=True)
    fecha_cambio = fields.Datetime(string='Fecha de Cambio', default=fields.Datetime.now, required=True)
    usuario_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user, required=True)
    comentario = fields.Text(string='Comentario del Cambio')
    tiempo_en_estado = fields.Float(string='Tiempo en Estado Anterior (horas)', compute='_compute_tiempo_en_estado')
    
    @api.depends('fecha_cambio', 'solicitud_id')
    def _compute_tiempo_en_estado(self):
        for record in self:
            if record.estado_anterior:
                # Buscar el cambio anterior
                cambio_anterior = self.search([
                    ('solicitud_id', '=', record.solicitud_id.id),
                    ('fecha_cambio', '<', record.fecha_cambio)
                ], order='fecha_cambio desc', limit=1)
                
                if cambio_anterior:
                    delta = record.fecha_cambio - cambio_anterior.fecha_cambio
                    record.tiempo_en_estado = delta.total_seconds() / 3600
                else:
                    # Si no hay cambio anterior, calcular desde la fecha de solicitud
                    delta = record.fecha_cambio - record.solicitud_id.fecha_solicitud
                    record.tiempo_en_estado = delta.total_seconds() / 3600
            else:
                record.tiempo_en_estado = 0

class PrioridadSolicitud(models.Model):
    _name = 'prioridad.solicitud'
    _description = 'Nivel de prioridad de la solicitud'
    _order = 'nivel desc'

    name = fields.Char(string='Nombre', required=True)
    nivel = fields.Integer(string='Nivel', required=True, help='1=Baja, 5=Crítica')
    descripcion = fields.Text(string='Descripción')
    color = fields.Char(string='Color', default='#FFFFFF')
    tiempo_respuesta_horas = fields.Integer(string='Tiempo de Respuesta (horas)', default=24)
    activo = fields.Boolean(string='Activo', default=True)
    
    @api.constrains('nivel')
    def _check_nivel(self):
        for record in self:
            if not 1 <= record.nivel <= 5:
                raise ValidationError('El nivel de prioridad debe estar entre 1 y 5.')

class ProveedorServicio(models.Model):
    _name = 'proveedor.servicio'
    _description = 'Proveedor externo de servicios'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código')
    contacto = fields.Char(string='Persona de Contacto')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')
    direccion = fields.Text(string='Dirección')
    sitio_web = fields.Char(string='Sitio Web')
    
    # Información comercial
    tipo_servicio = fields.Selection([
        ('mantenimiento', 'Mantenimiento'),
        ('tecnologia', 'Tecnología'),
        ('limpieza', 'Limpieza'),
        ('seguridad', 'Seguridad'),
        ('papeleria', 'Papelería'),
        ('otros', 'Otros'),
    ], string='Tipo de Servicio')
    
    calificacion = fields.Selection([
        ('1', 'Muy Malo'),
        ('2', 'Malo'),
        ('3', 'Regular'),
        ('4', 'Bueno'),
        ('5', 'Excelente'),
    ], string='Calificación')
    
    activo = fields.Boolean(string='Activo', default=True)
    notas = fields.Text(string='Notas')
    
    # Estadísticas
    total_servicios = fields.Integer(string='Total Servicios', compute='_compute_estadisticas')
    servicios_completados = fields.Integer(string='Servicios Completados', compute='_compute_estadisticas')
    
    @api.depends('name')
    def _compute_estadisticas(self):
        for record in self:
            solicitudes = self.env['solicitud.interna'].search([('proveedor_id', '=', record.id)])
            record.total_servicios = len(solicitudes)
            record.servicios_completados = len(solicitudes.filtered(lambda s: s.state in ['resuelto', 'cerrado']))

class ComentarioSolicitud(models.Model):
    _name = 'comentario.solicitud'
    _description = 'Comentario adicional sobre solicitud'
    _order = 'fecha desc'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True, ondelete='cascade')
    usuario_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user, required=True)
    comentario = fields.Html(string='Comentario', required=True)
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now, required=True)
    tipo = fields.Selection([
        ('interno', 'Interno'),
        ('publico', 'Público'),
        ('solucion', 'Solución'),
    ], string='Tipo', default='publico', required=True)
    
    # Adjuntos específicos del comentario
    attachment_ids = fields.Many2many('ir.attachment', string='Adjuntos')
    
    def name_get(self):
        result = []
        for record in self:
            name = f'{record.usuario_id.name} - {record.fecha.strftime("%d/%m/%Y %H:%M")}'
            result.append((record.id, name))
        return result

class EncuestaSatisfaccion(models.Model):
    _name = 'encuesta.satisfaccion'
    _description = 'Encuesta de satisfacción tras completar solicitud'
    _order = 'fecha desc'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True, ondelete='cascade')
    usuario_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user, required=True)
    
    # Puntuaciones específicas
    puntuacion_general = fields.Selection([
        ('1', 'Muy Insatisfecho'),
        ('2', 'Insatisfecho'),
        ('3', 'Neutral'),
        ('4', 'Satisfecho'),
        ('5', 'Muy Satisfecho'),
    ], string='Satisfacción General', required=True)
    
    puntuacion_tiempo = fields.Selection([
        ('1', 'Muy Lento'),
        ('2', 'Lento'),
        ('3', 'Aceptable'),
        ('4', 'Rápido'),
        ('5', 'Muy Rápido'),
    ], string='Tiempo de Respuesta')
    
    puntuacion_calidad = fields.Selection([
        ('1', 'Muy Mala'),
        ('2', 'Mala'),
        ('3', 'Aceptable'),
        ('4', 'Buena'),
        ('5', 'Excelente'),
    ], string='Calidad del Servicio')
    
    comentario = fields.Text(string='Comentarios Adicionales')
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now, required=True)
    recomendaria = fields.Boolean(string='¿Recomendaría el servicio?')
    
    # Campo calculado para promedio
    puntuacion_promedio = fields.Float(string='Puntuación Promedio', compute='_compute_puntuacion_promedio')
    
    @api.depends('puntuacion_general', 'puntuacion_tiempo', 'puntuacion_calidad')
    def _compute_puntuacion_promedio(self):
        for record in self:
            puntuaciones = []
            if record.puntuacion_general:
                puntuaciones.append(int(record.puntuacion_general))
            if record.puntuacion_tiempo:
                puntuaciones.append(int(record.puntuacion_tiempo))
            if record.puntuacion_calidad:
                puntuaciones.append(int(record.puntuacion_calidad))
            
            if puntuaciones:
                record.puntuacion_promedio = sum(puntuaciones) / len(puntuaciones)
            else:
                record.puntuacion_promedio = 0

# Modelo para plantillas de tickets
class PlantillaSolicitud(models.Model):
    _name = 'plantilla.solicitud'
    _description = 'Plantilla para crear solicitudes rápidamente'
    _order = 'name'

    name = fields.Char(string='Nombre de la Plantilla', required=True)
    descripcion = fields.Html(string='Descripción')
    category = fields.Selection([
        ('material', 'Material de Oficina'),
        ('soporte', 'Soporte Técnico'),
        ('mantenimiento', 'Mantenimiento'),
        ('permisos', 'Permisos'),
        ('rrhh', 'Recursos Humanos'),
        ('finanzas', 'Finanzas'),
        ('it', 'Tecnología'),
        ('otros', 'Otros'),
    ], string='Categoría', required=True)
    subcategory = fields.Char(string='Subcategoría')
    prioridad_id = fields.Many2one('prioridad.solicitud', string='Prioridad por Defecto')
    departamento_id = fields.Many2one('departamento.solicitud', string='Departamento por Defecto')
    gestor_id = fields.Many2one('res.users', string='Gestor por Defecto')
    activo = fields.Boolean(string='Activo', default=True)
    
    def crear_solicitud_desde_plantilla(self):
        """Método para crear una nueva solicitud basada en esta plantilla"""
        vals = {
            'name': self.name,
            'description': self.descripcion,
            'category': self.category,
            'subcategory': self.subcategory,
            'prioridad_id': self.prioridad_id.id if self.prioridad_id else False,
            'departamento_id': self.departamento_id.id if self.departamento_id else False,
            'gestor_id': self.gestor_id.id if self.gestor_id else False,
        }
        
        nueva_solicitud = self.env['solicitud.interna'].create(vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nueva Solicitud',
            'res_model': 'solicitud.interna',
            'res_id': nueva_solicitud.id,
            'view_mode': 'form',
            'target': 'current',
        }
