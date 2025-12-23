# Pruebas: solución al error de conexión a la base de datos

Este documento explica el error que apareció al ejecutar `pytest` y los pasos realizados para corregirlo.

Error observado

- Mensaje principal: `could not translate host name "db" to address: Temporary failure in name resolution`.
- Ocurre durante la importación de la aplicación en `test/conftest.py` porque en `Backend/app.py` se ejecuta `Base.metadata.create_all(bind=engine)` al importar la aplicación.
- `engine` se crea en `Backend/config/db.py` usando la variable de entorno `DATABASE_URL`. Si `DATABASE_URL` apunta a `postgres` en un contenedor llamado `db` (por ejemplo en `docker-compose`), ese hostname solo se resuelve dentro de la red de Docker Compose. Al ejecutar `pytest` localmente sin esa red, el hostname `db` no existe y la conexión falla.

Causa raíz

- La aplicación crea la conexión a la base de datos al importar los módulos (`create_engine(DATABASE_URL)` y `Base.metadata.create_all(bind=engine)`), lo que intenta conectarse antes de que los fixtures de prueba (que arrancan un contenedor de test) puedan establecer una base de datos accesible.

Resumen de acciones realizadas

1. Evité importar `app` a nivel de módulo en `test/conftest.py`. Importar `app` antes de tener `DATABASE_URL` configurada provoca la conexión fallida.
2. Modifiqué el fixture `postgres_container` para:
   - Iniciar `PostgresContainer` (de `testcontainers`).
   - Obtener la URL de conexión del contenedor y asignarla a la variable de entorno `DATABASE_URL`.
   - `yield` el contenedor y luego detenerlo en el teardown.
3. Importé `app` dentro del fixture `client`, de modo que la importación (y por ende `Base.metadata.create_all`) ocurre solo después de que `DATABASE_URL` apunte al contenedor de pruebas.
4. Añadí una inserción del directorio del proyecto en `sys.path` para asegurar que las importaciones locales funcionen desde la carpeta `test` cuando se ejecuta `pytest`.

Por qué esta solución funciona

- `testcontainers` levanta un contenedor PostgreSQL y nos da la URL de conexión (host, puerto mapeado, usuario, password). Si `app` se importa antes, intenta usar la configuración de producción (host `db`) y falla.
- Al establecer `os.environ['DATABASE_URL']` antes de importar `app`, el `engine` de SQLAlchemy se crea apuntando al contenedor de prueba, y `Base.metadata.create_all` se ejecuta correctamente contra esa base.

Notas y recomendaciones

- Alternativa robusta: evitar ejecutar `Base.metadata.create_all` en tiempo de importación de `app`. En su lugar, ejecutar la creación de tablas en el bloque `if __name__ == '__main__':` o mediante un comando separado (script de inicialización/migración). Esto evita efectos secundarios al importar la aplicación en tests o en otros contextos.

- Si los tests no desean levantar contenedores, otra opción es usar una base de datos SQLite en memoria durante pruebas y configurar `DATABASE_URL` en los tests para `sqlite:///:memory:`.

- Asegúrate de tener Docker corriendo cuando uses `testcontainers`.

Cómo reproducir localmente

```bash
cd Backend
# activar entorno virtual si procede
pytest test
```

Si ves errores de resolución de host (`db`), ejecuta Docker y asegúrate de que los tests usen `testcontainers` o ajusta `DATABASE_URL` para apuntar a una base local accesible.

---

Archivo modificado: `test/conftest.py` — la importación de `app` ahora se realiza dentro del fixture `client` y `DATABASE_URL` se configura a partir del contenedor de pruebas.
