from odoo import models, fields

class DepartamentoSolicitud(models.Model):
    _name = 'departamento.solicitud'
    _description = 'Departamento que puede hacer solicitudes'

    name = fields.Char(string='Nombre', required=True)
    responsable_id = fields.Many2one('res.users', string='Responsable')
    activo = fields.Boolean(string='Activo', default=True)

class TipoMaterial(models.Model):
    _name = 'tipo.material'
    _description = 'Tipo de material de oficina'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    stock_actual = fields.Integer(string='Stock Actual', default=0)

class HistorialEstadoSolicitud(models.Model):
    _name = 'historial.estado.solicitud'
    _description = 'Historial de cambios de estado de solicitudes'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True)
    estado_anterior = fields.Char(string='Estado Anterior')
    estado_nuevo = fields.Char(string='Estado Nuevo')
    fecha_cambio = fields.Datetime(string='Fecha de Cambio', default=fields.Datetime.now)
    usuario_id = fields.Many2one('res.users', string='Usuario')

class PrioridadSolicitud(models.Model):
    _name = 'prioridad.solicitud'
    _description = 'Nivel de prioridad de la solicitud'

    name = fields.Char(string='Nombre', required=True)
    nivel = fields.Integer(string='Nivel', required=True)
    descripcion = fields.Text(string='Descripción')

class ProveedorServicio(models.Model):
    _name = 'proveedor.servicio'
    _description = 'Proveedor externo de servicios'

    name = fields.Char(string='Nombre', required=True)
    contacto = fields.Char(string='Contacto')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')

class ComentarioSolicitud(models.Model):
    _name = 'comentario.solicitud'
    _description = 'Comentario adicional sobre solicitud'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True)
    usuario_id = fields.Many2one('res.users', string='Usuario')
    comentario = fields.Text(string='Comentario', required=True)
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now)

class EncuestaSatisfaccion(models.Model):
    _name = 'encuesta.satisfaccion'
    _description = 'Encuesta de satisfacción tras completar solicitud'

    solicitud_id = fields.Many2one('solicitud.interna', string='Solicitud', required=True)
    usuario_id = fields.Many2one('res.users', string='Usuario')
    puntuacion = fields.Integer(string='Puntuación')
    comentario = fields.Text(string='Comentario')
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now)
