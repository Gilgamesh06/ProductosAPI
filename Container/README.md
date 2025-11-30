# Container

## Despliegue

* **Ingresar** al directorio `Container`

    ```bash
    cd Container
    ```
    
* **Ejecutar** el siguiente comando para iniciar los servicios

    ```bash
    docker-compose up -d
    ```
    
* **Verificar** que los servicios esten corriendo

    ```bash
    docker-compose ps
    ``` 

## Detener los servicios

* **Detener** los servicios

    ```bash
    docker-compose down
    ```

* **Detener** los servicios y **eliminar** los contenedores

    ```bash
    docker-compose down --volumes
    ```

## Acceso

* A la API

    * Ruta: `http://localhost:8000/docs`

* A la base de datos

    * Ruta: `http://localhost:5435`
    * Usuario: `test`
    * Contraseña: `123456`
    * Base de datos: `productos_db`



