# Sistema de Tickets - Solicitudes Internas

## Descripción

Sistema completo de gestión de tickets para solicitudes internas en Odoo. Este módulo permite gestionar de manera eficiente las solicitudes de materiales, soporte técnico, mantenimiento y servicios dentro de una organización.

## Características Principales

### 🎫 Gestión de Tickets
- **Numeración automática**: Cada ticket recibe un número único (TK00001, TK00002, etc.)
- **Estados del ticket**: Borrador, Pendiente, Asignado, En Proceso, Esperando Respuesta, Resuelto, Cerrado, Cancelado
- **Categorías**: Material, Soporte, Mantenimiento, Servicio, Otros
- **Subcategorías**: Clasificación detallada por tipo de solicitud
- **Prioridades**: 5 niveles de prioridad con colores y tiempos de respuesta
- **Fechas de control**: Solicitud, asignación, inicio, límite, resolución y cierre

### 👥 Gestión de Usuarios
- **Roles definidos**:
  - **Solicitante**: Puede crear y ver sus propios tickets
  - **Gestor**: Puede gestionar todos los tickets, asignar, resolver y configurar el sistema
- **Asignación automática**: Los tickets pueden ser asignados a gestores específicos
- **Supervisión**: Control por departamentos con supervisores

### 📊 Seguimiento y Control
- **Historial de estados**: Registro completo de cambios de estado
- **Comentarios**: Sistema de comentarios internos y externos
- **Adjuntos**: Posibilidad de adjuntar archivos a los tickets
- **Tiempo de resolución**: Cálculo automático de tiempos
- **Alertas de vencimiento**: Identificación de tickets vencidos

### 🏢 Configuración Organizacional
- **Departamentos**: Gestión de departamentos con supervisores y presupuestos
- **Tipos de Material**: Catálogo de materiales con stock y precios
- **Proveedores**: Base de datos de proveedores de servicios
- **Plantillas**: Plantillas predefinidas para solicitudes comunes

### 📈 Reportes y Análisis
- **Vistas múltiples**: Lista, Kanban, Calendario, Gráficos, Tablas dinámicas
- **Filtros avanzados**: Búsqueda por múltiples criterios
- **Estadísticas**: Métricas de rendimiento por departamento y gestor
- **Encuestas de satisfacción**: Evaluación de la calidad del servicio

## Instalación

1. Copiar el módulo en la carpeta de addons de Odoo
2. Actualizar la lista de aplicaciones
3. Instalar el módulo "Sistema de Tickets - Solicitudes Internas"
4. Configurar usuarios y permisos según sea necesario

## Configuración Inicial

### 1. Usuarios y Permisos
- Asignar usuarios al grupo "Solicitante" o "Gestor de Solicitudes"
- Los gestores tienen acceso completo al sistema
- Los solicitantes solo pueden ver sus propios tickets

### 2. Configuración Básica
- **Departamentos**: Configurar los departamentos de la organización
- **Prioridades**: Ajustar niveles de prioridad y tiempos de respuesta
- **Tipos de Material**: Definir catálogo de materiales
- **Proveedores**: Registrar proveedores de servicios
- **Plantillas**: Crear plantillas para solicitudes frecuentes

### 3. Datos de Demostración
El módulo incluye datos de demostración que pueden ser útiles para:
- Entender el funcionamiento del sistema
- Realizar pruebas
- Servir como base para la configuración inicial

## Uso del Sistema

### Para Solicitantes
1. **Crear Ticket**: Acceder a "Tickets" > "Nuevo"
2. **Completar información**: Título, descripción, categoría, prioridad
3. **Enviar**: Cambiar estado a "Pendiente"
4. **Seguimiento**: Monitorear el progreso del ticket
5. **Evaluación**: Completar encuesta de satisfacción al cierre

### Para Gestores
1. **Revisar tickets**: Ver todos los tickets pendientes
2. **Asignar**: Asignar tickets a gestores específicos
3. **Procesar**: Cambiar estados según el progreso
4. **Resolver**: Documentar la solución implementada
5. **Cerrar**: Finalizar el ticket una vez confirmada la solución

## Flujo de Trabajo

```
Borrador → Pendiente → Asignado → En Proceso → Resuelto → Cerrado
                    ↓
                Esperando Respuesta
                    ↓
                En Proceso
```

### Estados Especiales
- **Cancelado**: Para tickets que no requieren procesamiento
- **Esperando Respuesta**: Cuando se requiere información adicional del solicitante

## Características Técnicas

### Modelos Principales
- `solicitud.interna`: Modelo principal de tickets
- `departamento.solicitud`: Departamentos organizacionales
- `prioridad.solicitud`: Niveles de prioridad
- `tipo.material`: Catálogo de materiales
- `proveedor.servicio`: Proveedores de servicios
- `plantilla.solicitud`: Plantillas de solicitudes
- `historial.estado.solicitud`: Historial de cambios
- `comentario.solicitud`: Sistema de comentarios
- `encuesta.satisfaccion`: Evaluaciones de satisfacción

### Integraciones
- **Mail**: Sistema de mensajería integrado
- **Portal**: Acceso desde portal web (si está configurado)
- **Attachments**: Gestión de archivos adjuntos
- **Chatter**: Sistema de seguimiento de actividades

## Personalización

El módulo está diseñado para ser fácilmente personalizable:
- Agregar nuevas categorías y subcategorías
- Modificar flujos de trabajo
- Añadir campos personalizados
- Integrar con otros módulos de Odoo

## Soporte

Para soporte técnico o consultas sobre el módulo, contactar al administrador del sistema.

## Versión

**Versión actual**: 2.0.0
**Compatible con**: Odoo 15.0+
**Última actualización**: 2024

---

*Este módulo ha sido desarrollado para proporcionar una solución completa y robusta de gestión de tickets internos, mejorando la eficiencia operativa y la satisfacción de los usuarios.*