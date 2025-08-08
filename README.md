# Sistema de Tickets - Solicitudes Internas con Odoo

Sistema completo de gestión de tickets para solicitudes internas desarrollado como módulo personalizado de Odoo.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Docker](#instalación-de-docker)
3. [Instalación de Docker Compose](#instalación-de-docker-compose)
4. [Configuración del Proyecto](#configuración-del-proyecto)
5. [Levantamiento del Contenedor](#levantamiento-del-contenedor)
6. [Configuración de Base de Datos](#configuración-de-base-de-datos)
7. [Acceso al Sistema](#acceso-al-sistema)
8. [Activación del Módulo](#activación-del-módulo)
9. [Uso del Sistema](#uso-del-sistema)
10. [Tablas del Módulo](#tablas-del-módulo)
11. [Características del Sistema](#características-del-sistema)
12. [Solución de Problemas](#solución-de-problemas)

## 🔧 Requisitos Previos

- Windows 10/11 (64-bit)
- Al menos 4GB de RAM disponible
- 10GB de espacio libre en disco
- Conexión a internet para descargar las imágenes de Docker

## 🐳 Instalación de Docker

### Paso 1: Descargar Docker Desktop

1. Visita [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Descarga Docker Desktop para Windows
3. Ejecuta el instalador descargado

### Paso 2: Instalar Docker Desktop

1. Ejecuta el archivo `.exe` descargado como administrador
2. Sigue las instrucciones del instalador
3. Asegúrate de marcar la opción "Use WSL 2 instead of Hyper-V"
4. Reinicia tu computadora cuando se te solicite

### Paso 3: Verificar la Instalación

1. Abre PowerShell como administrador
2. Ejecuta el siguiente comando:

```powershell
docker --version
```

Deberías ver algo como: `Docker version 24.0.x, build xxxxx`

## 🔗 Instalación de Docker Compose

Docker Compose viene incluido con Docker Desktop, pero puedes verificar su instalación:

```powershell
docker-compose --version
```

Deberías ver algo como: `Docker Compose version v2.x.x`

## ⚙️ Configuración del Proyecto

### Estructura del Proyecto

```
modulo_odoo/
├── README.md
├── docker-compose.yaml      # Configuración de contenedores
├── config/
│   └── odoo.conf            # Configuración de Odoo
└── addons/
    └── solicitud_interna/   # Módulo personalizado
        ├── __manifest__.py
        ├── models/
        ├── views/
        ├── security/
        └── data/
```

### Configuración de Puertos

- **Odoo**: Puerto 8200 (http://localhost:8200)
- **PostgreSQL**: Puerto 5432

## 🚀 Levantamiento del Contenedor

### Paso 1: Navegar al Directorio del Proyecto

```powershell
cd [RUTA_DE_TU_PROYECTO]\modulo_odoo
```

**Nota**: Reemplaza `[RUTA_DE_TU_PROYECTO]` con la ruta donde hayas descargado o clonado este proyecto.

**Ejemplo**:
```powershell
cd C:\Users\TuUsuario\Desktop\modulo_odoo
# o
cd D:\Proyectos\modulo_odoo
```

### Paso 2: Levantar los Servicios

```powershell
docker-compose up -d
```

Este comando:
- Descarga las imágenes necesarias (Odoo y PostgreSQL)
- Crea y configura los contenedores
- Inicia los servicios en segundo plano

### Paso 3: Verificar que los Contenedores Estén Ejecutándose

```powershell
docker-compose ps
```

Deberías ver algo como:
```
NAME   IMAGE          COMMAND                  SERVICE   CREATED         STATUS         PORTS
db     postgres:16.0  "docker-entrypoint.s…"   db        2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp
odoo   odoo:latest    "/entrypoint.sh odoo…"   odoo      2 minutes ago   Up 2 minutes   0.0.0.0:8200->8069/tcp
```

## 🗄️ Configuración de Base de Datos

La base de datos se configura automáticamente con los siguientes parámetros:

- **Base de datos**: `odoo`
- **Usuario**: `odoo`
- **Contraseña**: `odoo`
- **Host**: `db` (nombre del contenedor)

La configuración se encuentra en el archivo `docker-compose.yaml` y se aplica automáticamente al levantar los contenedores.

## 🔐 Acceso al Sistema

### URL de Acceso

**http://localhost:8200**

### Credenciales por Defecto

- **Usuario**: `admin`
- **Contraseña**: `admin`

### Primer Acceso

1. Abre tu navegador web
2. Navega a `http://localhost:8200`
3. Espera a que Odoo termine de inicializar (puede tomar unos minutos la primera vez)
4. Ingresa las credenciales:
   - Usuario: `admin`
   - Contraseña: `admin`
5. Haz clic en "Log in"

## 🔌 Activación del Módulo

### Paso 1: Acceder a la Lista de Aplicaciones

1. Una vez logueado, ve al menú principal
2. Haz clic en "Apps" (Aplicaciones)

### Paso 2: Buscar el Módulo

1. En la barra de búsqueda, escribe: `Sistema de Tickets`
2. Busca el módulo "Sistema de Tickets - Solicitudes Internas"

### Paso 3: Instalar el Módulo

1. Haz clic en el botón "Install" (Instalar)
2. Espera a que se complete la instalación
3. El sistema se recargará automáticamente

### Paso 4: Verificar la Instalación

Una vez instalado, deberías ver en el menú principal:
- **Solicitudes Internas** (nuevo menú)

## 📱 Uso del Sistema

### Menú Principal: Solicitudes Internas

El módulo agrega un nuevo menú con las siguientes opciones:

#### 📋 Gestión de Tickets
- **Mis Solicitudes**: Ver y gestionar tus propias solicitudes
- **Todas las Solicitudes**: Ver todas las solicitudes (para gestores)
- **Crear Solicitud**: Crear una nueva solicitud
- **Plantillas**: Gestionar plantillas de solicitudes

#### 📊 Reportes y Análisis
- **Dashboard**: Panel de control con métricas
- **Reportes**: Informes detallados
- **Encuestas de Satisfacción**: Resultados de encuestas

#### ⚙️ Configuración
- **Departamentos**: Gestionar departamentos
- **Prioridades**: Configurar niveles de prioridad
- **Tipos de Material**: Catálogo de materiales
- **Proveedores**: Gestionar proveedores de servicios

### Flujo de Trabajo Típico

1. **Crear Solicitud**:
   - Ir a "Crear Solicitud"
   - Llenar el formulario con título, descripción, categoría
   - Seleccionar prioridad y departamento
   - Guardar

2. **Seguimiento**:
   - La solicitud pasa por estados: Pendiente → Asignado → En Proceso → Resuelto → Cerrado
   - Se pueden agregar comentarios y adjuntos
   - Se registra historial completo de cambios

3. **Resolución**:
   - El gestor asignado trabaja en la solicitud
   - Se documenta la solución aplicada
   - Se cierra el ticket
   - Opcionalmente se solicita encuesta de satisfacción

## 🗃️ Tablas del Módulo

El módulo crea las siguientes tablas en la base de datos:

### Tabla Principal
- **`solicitud_interna`**: Tabla principal de tickets/solicitudes

### Tablas de Configuración
- **`departamento_solicitud`**: Departamentos que pueden hacer solicitudes
- **`prioridad_solicitud`**: Niveles de prioridad (Baja, Media, Alta, Urgente, Crítica)
- **`tipo_material`**: Catálogo de tipos de materiales de oficina
- **`proveedor_servicio`**: Proveedores externos de servicios
- **`plantilla_solicitud`**: Plantillas para crear solicitudes rápidamente

### Tablas de Seguimiento
- **`historial_estado_solicitud`**: Historial completo de cambios de estado
- **`comentario_solicitud`**: Comentarios adicionales en las solicitudes
- **`encuesta_satisfaccion`**: Encuestas de satisfacción post-resolución

### Campos Principales de `solicitud_interna`

- **Identificación**: `numero_ticket`, `name` (título)
- **Categorización**: `category`, `subcategory`
- **Estados**: `state` (borrador, pendiente, asignado, en_proceso, esperando_respuesta, resuelto, cerrado, cancelado)
- **Fechas**: `fecha_solicitud`, `fecha_asignacion`, `fecha_limite`, `fecha_resolucion`, `fecha_cierre`
- **Usuarios**: `solicitante_id`, `gestor_id`, `supervisor_id`
- **Relaciones**: `departamento_id`, `prioridad_id`, `tipo_material_id`, `proveedor_id`
- **Seguimiento**: `tiempo_resolucion`, `costo_estimado`, `costo_real`
- **Satisfacción**: `puntuacion_satisfaccion`

## ✨ Características del Sistema

### 🎯 Funcionalidades Principales

- **Gestión Completa de Tickets**: Creación, asignación, seguimiento y cierre
- **Sistema de Estados Avanzado**: 8 estados diferentes con transiciones controladas
- **Múltiples Categorías**: Material de oficina, soporte técnico, mantenimiento, etc.
- **Sistema de Prioridades**: 5 niveles de prioridad con colores distintivos
- **Seguimiento de Tiempos**: Métricas de tiempo de resolución y SLA
- **Historial Completo**: Registro detallado de todos los cambios
- **Sistema de Comentarios**: Comentarios internos y públicos
- **Adjuntos**: Soporte para archivos adjuntos
- **Encuestas de Satisfacción**: Evaluación post-resolución
- **Plantillas**: Creación rápida de solicitudes recurrentes

### 👥 Roles de Usuario

- **Solicitante**: Puede crear y seguir sus propias solicitudes
- **Gestor**: Puede gestionar todas las solicitudes y configuraciones
- **Administrador**: Acceso completo al sistema

### 📊 Vistas Disponibles

- **Vista Kanban**: Tablero visual por estados
- **Vista Lista**: Listado detallado con filtros
- **Vista Formulario**: Formulario completo de solicitud
- **Vista Calendario**: Visualización por fechas
- **Vista Gráficos**: Reportes y análisis

## 🔧 Comandos Útiles

### Gestión de Contenedores

```powershell
# Levantar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs de Odoo
docker-compose logs odoo

# Ver logs de PostgreSQL
docker-compose logs db

# Reiniciar solo Odoo
docker-compose restart odoo

# Ver estado de contenedores
docker-compose ps
```

### Acceso a Contenedores

```powershell
# Acceder al contenedor de Odoo
docker-compose exec odoo bash

# Acceder al contenedor de PostgreSQL
docker-compose exec db psql -U odoo -d odoo
```

## 🛠️ Solución de Problemas

### Problema: No se puede acceder a http://localhost:8200

**Solución**:
1. Verificar que los contenedores estén ejecutándose: `docker-compose ps`
2. Verificar los logs: `docker-compose logs odoo`
3. Esperar unos minutos más (la primera inicialización puede ser lenta)

### Problema: Error de conexión a la base de datos

**Solución**:
1. Verificar que el contenedor de PostgreSQL esté ejecutándose
2. Reiniciar los servicios: `docker-compose down && docker-compose up -d`

### Problema: El módulo no aparece en la lista de aplicaciones

**Solución**:
1. Verificar que la carpeta `addons/solicitud_interna` esté presente
2. Actualizar la lista de aplicaciones en Odoo:
   - Ir a Apps → Update Apps List
3. Reiniciar Odoo: `docker-compose restart odoo`

### Problema: Cambios en el código no se reflejan

**Solución**:
1. Reiniciar el contenedor de Odoo: `docker-compose restart odoo`
2. Si persiste, actualizar el módulo desde la interfaz de Odoo

### Problema: Puertos ocupados

**Solución**:
1. Cambiar los puertos en `docker-compose.yaml`
2. Por ejemplo, cambiar `"8200:8069"` por `"8201:8069"`
3. Acceder entonces a `http://localhost:8201`

## 📞 Soporte

Para soporte adicional:

1. Revisar los logs: `docker-compose logs`
2. Verificar la documentación oficial de Odoo
3. Consultar la comunidad de Odoo

---

**¡El sistema está listo para usar!** 🎉

Accede a **http://localhost:8200** con usuario `admin` y contraseña `admin` para comenzar a gestionar tus solicitudes internas.

