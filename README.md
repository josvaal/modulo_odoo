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

## 📱 Guía de Uso para Usuario Final

### 🏠 Navegación Principal

Una vez que ingreses al sistema, verás el menú principal de Odoo. Busca y haz clic en **"Solicitudes Internas"** para acceder al sistema de tickets.

### 📋 Panel de Control - Mis Solicitudes

Al entrar al módulo, la primera pantalla que verás es **"Mis Solicitudes"**, donde puedes:

- 📊 **Ver el resumen** de todas tus solicitudes
- 🔍 **Filtrar** por estado (Pendiente, En Proceso, Resuelto, etc.)
- 📅 **Ordenar** por fecha, prioridad o estado
- 👁️ **Ver detalles** haciendo clic en cualquier solicitud

### ➕ Cómo Crear una Nueva Solicitud

#### Paso 1: Acceder al Formulario
1. Haz clic en el botón **"Crear"** (generalmente en la esquina superior izquierda)
2. Se abrirá el formulario de nueva solicitud

#### Paso 2: Llenar la Información Básica
**Campos Obligatorios:**
- **📝 Título**: Escribe un título claro y descriptivo
  - ✅ Ejemplo bueno: "Solicitud de papel para impresora oficina 3"
  - ❌ Ejemplo malo: "Necesito algo"

- **📄 Descripción**: Explica detalladamente tu solicitud
  - Incluye: ¿Qué necesitas? ¿Para cuándo? ¿Cantidad? ¿Ubicación?
  - Ejemplo: "Necesito 5 resmas de papel tamaño carta para la impresora de la oficina 3, segundo piso. Es urgente porque se nos acabó y tenemos que imprimir reportes para la reunión del viernes."

- **🏷️ Categoría**: Selecciona la categoría que mejor describa tu solicitud:
  - 📎 **Material de Oficina**: Papel, bolígrafos, carpetas, etc.
  - 🔧 **Soporte Técnico**: Problemas con computadora, impresora, software
  - 🛠️ **Mantenimiento**: Reparaciones, limpieza, instalaciones
  - 📋 **Permisos**: Solicitudes de autorización o permisos especiales
  - 👥 **Recursos Humanos**: Vacaciones, capacitaciones, documentos
  - 💰 **Finanzas**: Reembolsos, pagos, presupuestos
  - 💻 **Tecnología**: Software nuevo, accesos, equipos
  - 📦 **Otros**: Cualquier otra solicitud

- **🏢 Departamento**: Selecciona tu departamento
- **⚡ Prioridad**: Elige el nivel de urgencia:
  - 🟢 **Baja**: No es urgente, puede esperar semanas
  - 🟡 **Media**: Importante, necesario en unos días
  - 🟠 **Alta**: Urgente, necesario pronto
  - 🔴 **Urgente**: Muy urgente, necesario hoy o mañana
  - 🚨 **Crítica**: Emergencia, bloquea el trabajo

#### Paso 3: Información Adicional (Opcional)
- **📅 Fecha Límite**: Si tienes una fecha específica cuando lo necesitas
- **💵 Costo Estimado**: Si conoces el costo aproximado
- **📎 Adjuntos**: Puedes subir imágenes, documentos o archivos relacionados

#### Paso 4: Guardar la Solicitud
1. Haz clic en **"Guardar"**
2. Tu solicitud se creará con un número único (ej: SOL-2024-001)
3. Recibirás una notificación de confirmación

### 📊 Estados de las Solicitudes - ¿Qué Significan?

Tus solicitudes pasarán por diferentes estados. Aquí te explicamos cada uno:

- **📝 Borrador**: Solicitud que estás creando pero aún no has enviado
- **⏳ Pendiente**: Solicitud enviada, esperando ser asignada a un gestor
- **👤 Asignado**: Ya tiene un gestor responsable que se encargará
- **⚙️ En Proceso**: El gestor está trabajando en tu solicitud
- **💬 Esperando Respuesta**: Necesitan más información de tu parte
- **✅ Resuelto**: La solicitud está completa, esperando tu confirmación
- **🔒 Cerrado**: Solicitud completamente terminada
- **❌ Cancelado**: Solicitud cancelada por algún motivo

### 🔍 Cómo Hacer Seguimiento a tus Solicitudes

#### Ver el Estado Actual
1. Ve a **"Mis Solicitudes"**
2. Busca tu solicitud en la lista
3. El estado actual aparece en una etiqueta de color

#### Ver Detalles Completos
1. Haz clic en el **título** de tu solicitud
2. Se abrirá la vista detallada donde puedes ver:
   - 📋 Toda la información de la solicitud
   - 📝 Historial de cambios
   - 💬 Comentarios del gestor
   - 📎 Archivos adjuntos
   - ⏱️ Tiempos de respuesta

#### Agregar Comentarios
1. En la vista detallada, busca la sección **"Comentarios"**
2. Escribe tu comentario en el campo de texto
3. Haz clic en **"Enviar"**
4. El gestor recibirá una notificación

### 💬 Comunicación con el Gestor

#### Cuándo Comentar:
- ✅ Para proporcionar información adicional
- ✅ Para aclarar dudas
- ✅ Para cambiar algún detalle de la solicitud
- ✅ Para preguntar sobre el progreso
- ✅ Para agradecer cuando se resuelva

#### Cómo Escribir Buenos Comentarios:
- 📝 Sé claro y específico
- 📅 Menciona fechas si son importantes
- 📍 Incluye ubicaciones si es relevante
- 🙏 Mantén un tono profesional y amable

**Ejemplo de buen comentario:**
"Hola, quería agregar que necesito el papel antes del jueves porque tenemos una presentación importante. Si no es posible, por favor avísame para buscar alternativas. ¡Gracias!"

### 📎 Cómo Subir Archivos Adjuntos

1. En el formulario de solicitud o en los comentarios
2. Busca el botón **"Adjuntar Archivo"** o el ícono 📎
3. Haz clic y selecciona el archivo desde tu computadora
4. Espera a que se suba completamente
5. El archivo aparecerá en la lista de adjuntos

**Tipos de archivos útiles:**
- 📷 Fotos del problema (para soporte técnico)
- 📄 Documentos de referencia
- 📊 Cotizaciones o presupuestos
- 🖼️ Capturas de pantalla

### 🔔 Notificaciones - Mantente Informado

Recibirás notificaciones automáticas cuando:
- ✅ Tu solicitud sea asignada a un gestor
- 💬 El gestor agregue comentarios
- 🔄 Cambie el estado de tu solicitud
- ✅ Tu solicitud sea resuelta
- 📋 Se requiera tu feedback

### 📊 Vista Kanban - Visualización por Estados

1. En **"Mis Solicitudes"**, cambia a vista **"Kanban"**
2. Verás columnas por cada estado
3. Tus solicitudes aparecen como tarjetas
4. Puedes arrastrar y soltar para cambiar estados (si tienes permisos)

### 🎯 Plantillas - Solicitudes Rápidas

Si haces solicitudes similares frecuentemente:

1. Ve a **"Plantillas"** en el menú
2. Busca plantillas predefinidas para tu tipo de solicitud
3. Haz clic en **"Usar Plantilla"**
4. Se creará una solicitud con información prellenada
5. Solo modifica lo que necesites y guarda

### 📈 Dashboard - Tu Resumen Personal

En el **Dashboard** puedes ver:
- 📊 Gráficos de tus solicitudes por estado
- 📅 Solicitudes recientes
- ⏱️ Tiempos promedio de resolución
- 🎯 Estadísticas de satisfacción

### ⭐ Encuesta de Satisfacción

Cuando tu solicitud se resuelva:

1. Recibirás una invitación para evaluar el servicio
2. Califica del 1 al 5:
   - 🌟 Satisfacción general
   - ⏱️ Tiempo de respuesta
   - 🎯 Calidad del servicio
3. Agrega comentarios opcionales
4. Tu feedback ayuda a mejorar el servicio

### 🆘 ¿Necesitas Ayuda?

#### Si tu solicitud está tomando mucho tiempo:
1. Revisa el estado actual
2. Agrega un comentario preguntando por el progreso
3. Si es urgente, menciona la fecha límite

#### Si necesitas cambiar algo en tu solicitud:
1. Agrega un comentario explicando el cambio
2. Si es un cambio mayor, considera crear una nueva solicitud

#### Si no encuentras tu solicitud:
1. Usa los filtros en **"Mis Solicitudes"**
2. Busca por número de ticket o título
3. Revisa si está en estado "Borrador"

### 💡 Consejos para Mejores Resultados

#### ✅ Buenas Prácticas:
- 📝 Sé específico en títulos y descripciones
- 📅 Proporciona fechas límite realistas
- 📎 Adjunta fotos o documentos cuando sea útil
- 💬 Responde rápidamente a las preguntas del gestor
- 🙏 Mantén comunicación profesional y amable
- ⭐ Completa las encuestas de satisfacción

#### ❌ Evita:
- 📝 Títulos vagos como "Ayuda" o "Problema"
- 🚨 Marcar todo como "Crítico" si no lo es
- 📞 Crear múltiples solicitudes para lo mismo
- 💬 Comentarios innecesarios o muy frecuentes
- 😤 Lenguaje agresivo o demandante

### 📱 Acceso Móvil

Puedes acceder al sistema desde tu teléfono:
1. Abre el navegador en tu móvil
2. Ve a la misma dirección: http://localhost:8200
3. Inicia sesión normalmente
4. La interfaz se adaptará a tu pantalla

---

**¡Recuerda!** 🎯
El sistema está diseñado para hacer tu trabajo más fácil. Si tienes dudas, no dudes en crear una solicitud de "Soporte Técnico" para que te ayuden con el uso del sistema.

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

## 🧪 Pruebas Cáusticas del Sistema

### 🎯 ¿Qué son las Pruebas Cáusticas?

Las pruebas cáusticas son pruebas exhaustivas diseñadas para "romper" el sistema y encontrar sus límites. Estas pruebas simulan condiciones extremas, errores de usuario y situaciones inesperadas para garantizar que el sistema sea robusto y confiable.

### 📋 Lista de Pruebas a Realizar

#### 🔥 Pruebas de Estrés y Límites

**1. Prueba de Volumen de Solicitudes**
```powershell
# Crear múltiples solicitudes simultáneamente
# Objetivo: Probar el rendimiento con alta carga
```
- Crear 100+ solicitudes en un período corto
- Verificar que el sistema no se ralentice
- Comprobar que todas las solicitudes se guarden correctamente
- Validar que los números de ticket sean únicos

**2. Prueba de Campos con Datos Extremos**
- **Títulos muy largos**: Crear solicitud con título de 1000+ caracteres
- **Descripciones masivas**: Descripción con 10,000+ caracteres
- **Caracteres especiales**: Usar emojis, símbolos, acentos, caracteres Unicode
- **Campos vacíos**: Intentar guardar con campos obligatorios vacíos

**3. Prueba de Archivos Adjuntos**
- Subir archivos de diferentes tipos: PDF, DOC, XLS, IMG, ZIP
- Probar archivos muy grandes (>50MB)
- Subir archivos con nombres especiales: espacios, acentos, símbolos
- Intentar subir archivos corruptos
- Subir múltiples archivos simultáneamente

#### 💥 Pruebas de Casos Extremos

**4. Prueba de Estados Inválidos**
- Intentar cambiar estados de forma no secuencial
- Probar transiciones de estado no permitidas
- Verificar que solo usuarios autorizados puedan cambiar estados

**5. Prueba de Fechas Extremas**
- Fechas límite en el pasado
- Fechas muy lejanas en el futuro (año 2099)
- Fechas inválidas (30 de febrero)
- Cambios de zona horaria

**6. Prueba de Usuarios y Permisos**
- Acceso con usuario sin permisos
- Intentar modificar solicitudes de otros usuarios
- Probar con usuario desactivado
- Sesiones simultáneas del mismo usuario

#### 🌐 Pruebas de Navegadores y Dispositivos

**7. Compatibilidad de Navegadores**
- Chrome (última versión)
- Firefox (última versión)
- Edge (última versión)
- Safari (si tienes Mac)
- Navegadores móviles

**8. Pruebas de Responsividad**
- Pantallas muy pequeñas (320px)
- Pantallas muy grandes (4K)
- Orientación vertical y horizontal en móviles
- Zoom del navegador al 50% y 200%

#### 🔒 Pruebas de Seguridad

**9. Pruebas de Inyección**
- Intentar inyectar código HTML en campos de texto
- Probar scripts JavaScript en formularios
- Caracteres SQL en campos de búsqueda

**10. Pruebas de Autenticación**
- Intentar acceder sin estar logueado
- Probar con credenciales incorrectas múltiples veces
- Verificar timeout de sesión

### 🧪 Cómo Ejecutar las Pruebas

#### Preparación del Entorno de Pruebas

**1. Levantar el Sistema**
```powershell
cd [RUTA_DE_TU_PROYECTO]\modulo_odoo
docker-compose up -d
```

**2. Verificar que Todo Esté Funcionando**
```powershell
docker-compose ps
# Ambos contenedores deben estar "Up"
```

**3. Acceder al Sistema**
- URL: http://localhost:8200
- Usuario: admin
- Contraseña: admin

#### 📝 Ejecución de Pruebas Paso a Paso

**Prueba 1: Sobrecarga de Solicitudes**
1. Abrir múltiples pestañas del navegador (10+)
2. En cada pestaña, crear una solicitud simultáneamente
3. Verificar que todas se guarden correctamente
4. Comprobar que no haya números de ticket duplicados

**Resultado Esperado**: ✅ Todas las solicitudes se crean sin errores

**Prueba 2: Campos con Datos Extremos**
1. Crear solicitud con título de 500+ caracteres
2. Descripción con texto muy largo (copiar/pegar un artículo completo)
3. Usar caracteres especiales: áéíóú, ñ, ¿¡, €, @, #, %, &
4. Intentar guardar

**Resultado Esperado**: ✅ El sistema maneja los datos sin errores o muestra validaciones apropiadas

**Prueba 3: Archivos Problemáticos**
1. Crear un archivo de texto de 100MB
2. Intentar subirlo como adjunto
3. Probar con archivo .exe
4. Archivo con nombre "archivo con espacios y acentos ñáéí.pdf"

**Resultado Esperado**: ✅ El sistema rechaza archivos no permitidos o muy grandes con mensajes claros

**Prueba 4: Navegación Agresiva**
1. Hacer clic rápidamente en múltiples botones
2. Usar el botón "Atrás" del navegador en medio de un proceso
3. Refrescar la página mientras se guarda una solicitud
4. Cerrar el navegador y volver a abrir

**Resultado Esperado**: ✅ El sistema mantiene la consistencia de datos

**Prueba 5: Estados y Transiciones**
1. Crear una solicitud
2. Intentar cambiarla directamente de "Pendiente" a "Cerrado"
3. Probar cambios de estado sin ser el gestor asignado
4. Intentar modificar solicitudes muy antiguas

**Resultado Esperado**: ✅ Solo se permiten transiciones válidas según las reglas de negocio

#### 🔍 Pruebas de Rendimiento

**Prueba de Carga de Datos**
1. Crear 1000+ solicitudes usando plantillas
2. Medir tiempo de carga de la vista "Todas las Solicitudes"
3. Probar filtros y búsquedas con gran volumen de datos
4. Verificar que los reportes se generen en tiempo razonable

**Comandos para Monitoreo**
```powershell
# Ver uso de recursos
docker stats

# Ver logs en tiempo real
docker-compose logs -f odoo

# Ver logs de errores
docker-compose logs odoo | findstr ERROR
```

### 📊 Registro de Resultados

#### Plantilla de Reporte de Pruebas

```
=== REPORTE DE PRUEBAS CÁUSTICAS ===
Fecha: [FECHA]
Versión del Sistema: [VERSIÓN]
Navegador: [NAVEGADOR Y VERSIÓN]

PRUEBA 1: Sobrecarga de Solicitudes
- Estado: [PASÓ/FALLÓ]
- Observaciones: [DETALLES]
- Tiempo de respuesta: [SEGUNDOS]

PRUEBA 2: Datos Extremos
- Estado: [PASÓ/FALLÓ]
- Observaciones: [DETALLES]
- Errores encontrados: [LISTA]

[... continuar para todas las pruebas]

RESUMEN:
- Total de pruebas: [NÚMERO]
- Pruebas exitosas: [NÚMERO]
- Pruebas fallidas: [NÚMERO]
- Errores críticos: [NÚMERO]
- Errores menores: [NÚMERO]
```

### 🚨 Qué Hacer Si Encuentras Errores

#### Errores Críticos (Sistema No Funciona)
1. **Capturar evidencia**:
   - Screenshot del error
   - Logs del sistema: `docker-compose logs odoo`
   - Pasos exactos para reproducir

2. **Reiniciar servicios**:
   ```powershell
   docker-compose restart odoo
   ```

3. **Si persiste**:
   ```powershell
   docker-compose down
   docker-compose up -d
   ```

#### Errores Menores (Funcionalidad Limitada)
1. Documentar el comportamiento inesperado
2. Verificar si es un problema de configuración
3. Probar en diferentes navegadores
4. Revisar permisos de usuario

### 🎯 Criterios de Aceptación

**El sistema PASA las pruebas cáusticas si:**

✅ **Estabilidad**: No se cuelga ni se vuelve inaccesible
✅ **Integridad de Datos**: No se pierden ni corrompen datos
✅ **Seguridad**: No permite accesos no autorizados
✅ **Rendimiento**: Responde en menos de 5 segundos bajo carga normal
✅ **Usabilidad**: Los errores muestran mensajes claros y útiles
✅ **Recuperación**: Se recupera automáticamente de errores temporales

**El sistema FALLA si:**

❌ Se cuelga o se vuelve inaccesible
❌ Se pierden datos o solicitudes
❌ Permite acceso no autorizado a información
❌ Tarda más de 30 segundos en responder
❌ Muestra errores técnicos incomprensibles al usuario
❌ Requiere reinicio manual para funcionar

### 🔄 Automatización de Pruebas (Avanzado)

Para equipos técnicos, se pueden crear scripts de automatización:

```powershell
# Script básico de prueba de conectividad
$response = Invoke-WebRequest -Uri "http://localhost:8200" -UseBasicParsing
if ($response.StatusCode -eq 200) {
    Write-Host "✅ Sistema accesible" -ForegroundColor Green
} else {
    Write-Host "❌ Sistema no responde" -ForegroundColor Red
}
```

### 📈 Métricas de Rendimiento

**Benchmarks Recomendados:**
- Tiempo de carga inicial: < 3 segundos
- Creación de solicitud: < 2 segundos
- Búsqueda/filtrado: < 1 segundo
- Carga de reportes: < 10 segundos
- Subida de archivos (10MB): < 30 segundos

---

**💡 Consejo**: Ejecuta estas pruebas regularmente, especialmente después de actualizaciones o cambios en el sistema. Un sistema que pasa las pruebas cáusticas es un sistema confiable para producción.

### 🚀 Scripts Automatizados de Pruebas

Para facilitar la ejecución de las pruebas cáusticas, se han creado varios scripts automatizados:

#### 📁 Archivos de Pruebas Disponibles

| Archivo | Descripción | Uso Recomendado |
|---------|-------------|------------------|
| `ejecutar_pruebas.bat` | **Menú interactivo** - Fácil de usar | Principiantes, uso ocasional |
| `ejecutar_pruebas_causticas.ps1` | **Pruebas completas** con reporte HTML detallado | Validación exhaustiva, pre-producción |
| `pruebas_causticas_simple.ps1` | **Pruebas básicas** rápidas (30 segundos) | Verificación diaria, monitoreo |
| `GUIA_PRUEBAS_CAUSTICAS.md` | **Documentación completa** de las pruebas | Referencia y troubleshooting |

#### 🖱️ Ejecución Rápida

**Método más fácil (Recomendado):**
1. Hacer **doble clic** en `ejecutar_pruebas.bat`
2. Seleccionar el tipo de prueba desde el menú
3. Esperar los resultados

**Desde PowerShell:**
```powershell
# Pruebas completas (3-5 minutos)
.\ejecutar_pruebas_causticas.ps1

# Pruebas rápidas (30 segundos)
.\pruebas_causticas_simple.ps1

# Con parámetros personalizados
.\ejecutar_pruebas_causticas.ps1 -QuickTest -ReportPath "mi_reporte.html"
```

#### 📊 Tipos de Reportes Generados

- **Reporte HTML Completo**: Análisis detallado con gráficos y estadísticas
- **Reporte Simple**: Resumen en texto plano para logs automáticos
- **Resultados en Consola**: Feedback inmediato durante la ejecución

#### 🎯 Códigos de Resultado

| Código | Estado | Significado |
|--------|--------|--------------|
| **0** | ✅ APROBADO | Sistema funcionando correctamente |
| **1** | ⚠️ CON ADVERTENCIAS | Problemas menores detectados |
| **2** | ❌ RECHAZADO | Errores críticos encontrados |

**Para más información detallada, consulta: `GUIA_PRUEBAS_CAUSTICAS.md`**

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

