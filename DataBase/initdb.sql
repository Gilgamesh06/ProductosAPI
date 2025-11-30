-- Script de inicialización de datos para ProductosApi
-- Este script se ejecuta DESPUÉS de que FastAPI crea las tablas

-- Insertar categorías de prueba
INSERT INTO categoria (nombre, estado, fecha_creacion) VALUES
    ('Electrónica', 'ACTIVO', NOW()),
    ('Alimentos', 'ACTIVO', NOW()),
    ('Bebidas', 'ACTIVO', NOW()),
    ('Hogar', 'ACTIVO', NOW()),
    ('Deportes', 'ACTIVO', NOW())
ON CONFLICT (nombre) DO NOTHING;

-- Insertar productos de prueba
INSERT INTO producto (nombre, precio, cantidad, fecha_vencimiento, categoria_id, estado, fecha_creacion) 
SELECT 
    nombre, precio, cantidad, fecha_vencimiento::timestamp, 
    (SELECT id FROM categoria WHERE nombre = cat_nombre), 
    'ACTIVO', NOW()
FROM (VALUES
    ('Laptop Dell XPS 13', 45000, 10, '2026-12-31', 'Electrónica'),
    ('Mouse Logitech', 1500, 50, '2027-06-30', 'Electrónica'),
    ('Arroz Premium 1kg', 120, 200, '2025-12-31', 'Alimentos'),
    ('Aceite de Oliva 500ml', 350, 80, '2026-03-15', 'Alimentos'),
    ('Coca Cola 2L', 80, 150, '2025-08-20', 'Bebidas'),
    ('Agua Mineral 1.5L', 45, 300, '2026-01-10', 'Bebidas'),
    ('Toallas de Baño', 250, 40, '2028-12-31', 'Hogar'),
    ('Balón de Fútbol', 450, 25, '2027-11-30', 'Deportes'),
    ('Raqueta de Tenis', 1200, 15, '2027-09-15', 'Deportes'),
    ('Smartphone Samsung', 25000, 20, '2026-10-31', 'Electrónica')
) AS datos(nombre, precio, cantidad, fecha_vencimiento, cat_nombre)
WHERE NOT EXISTS (
    SELECT 1 FROM producto WHERE producto.nombre = datos.nombre
);

-- Insertar un producto inactivo para pruebas
INSERT INTO producto (nombre, precio, cantidad, fecha_vencimiento, categoria_id, estado, fecha_creacion, fecha_borrado) 
SELECT 
    'Producto Descontinuado', 100, 0, '2024-01-01'::timestamp,
    (SELECT id FROM categoria WHERE nombre = 'Alimentos'), 
    'INACTIVO', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM producto WHERE nombre = 'Producto Descontinuado'
);

-- Insertar una categoría inactiva para pruebas
INSERT INTO categoria (nombre, estado, fecha_creacion, fecha_borrado) 
SELECT 'Categoría Obsoleta', 'INACTIVO', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM categoria WHERE nombre = 'Categoría Obsoleta'
);
