-- Tablas adicionales para el módulo solicitud_interna

-- 1. Departamentos que pueden hacer solicitudes
CREATE TABLE departamento_solicitud (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    responsable_id INTEGER REFERENCES res_users(id),
    activo BOOLEAN DEFAULT TRUE
);

-- 2. Tipos de materiales de oficina
CREATE TABLE tipo_material (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    stock_actual INTEGER DEFAULT 0
);

-- 3. Historial de cambios de estado de solicitudes
CREATE TABLE historial_estado_solicitud (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL,
    estado_anterior VARCHAR(30),
    estado_nuevo VARCHAR(30),
    fecha_cambio TIMESTAMP DEFAULT NOW(),
    usuario_id INTEGER REFERENCES res_users(id)
);

-- 4. Niveles de prioridad para solicitudes
CREATE TABLE prioridad_solicitud (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    nivel INTEGER NOT NULL,
    descripcion TEXT
);

-- 5. Proveedores externos de servicios
CREATE TABLE proveedor_servicio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(30),
    email VARCHAR(100)
);

-- 6. Comentarios adicionales sobre solicitudes
CREATE TABLE comentario_solicitud (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL,
    usuario_id INTEGER REFERENCES res_users(id),
    comentario TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT NOW()
);

-- 7. Encuestas de satisfacción tras completar solicitudes
CREATE TABLE encuesta_satisfaccion (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL,
    usuario_id INTEGER REFERENCES res_users(id),
    puntuacion INTEGER CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    fecha TIMESTAMP DEFAULT NOW()
);
