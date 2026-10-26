# Objetos Perdidos y Encontrados

Aplicación web hecha con Flask para registrar objetos perdidos y encontrados, consultarlos por estado y detectar posibles coincidencias entre ellos. La interfaz (HTML y CSS) se sirve desde la misma aplicación y los datos se guardan en un archivo JSON.

## Funcionalidades

- **Registrar** un objeto como perdido o encontrado.
- **Listar** los objetos según su estado: perdido, encontrado o recuperado.
- **Buscar coincidencias** entre objetos perdidos y encontrados por tipo y color, desde la pantalla de listado.
- **Marcar** un objeto perdido como recuperado.

## Estructura

```
.
├── app.py             # Rutas de la aplicación y de la API
├── service.py         # Lógica de negocio y acceso al JSON
├── requirements.txt   # Dependencias de Python
├── Dockerfile         # Imagen de la aplicación
├── data/
│   └── objetos.json   # Almacenamiento de los objetos
├── templates/         # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── registrar.html
│   └── listar.html
├── static/
│   └── estilos.css    # Estilos
└── docs/
    └── api-contract.md  # Contrato de la API
```

## Ejecución local

```bash
python -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

La carpeta `data/` debe existir; si no, el registro de objetos responde con error 500.

## Ejecución con Docker

Construir la imagen:

```bash
docker build -t objetos-perdidos .
```

Ejecutar el contenedor:

```bash
docker run -d --name objetos-perdidos -p 5000:5000 -v "$(pwd)/data:/app/data" objetos-perdidos
```

El volumen (`-v`) conserva los objetos en la carpeta local `data/`, por lo que no se pierden al detener o recrear el contenedor. En Windows PowerShell se usa `${PWD}` en lugar de `$(pwd)`.

Para detener y eliminar el contenedor:

```bash
docker stop objetos-perdidos
docker rm objetos-perdidos
```

En ambos casos la aplicación queda disponible en `http://localhost:5000`.

## API

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/items` | Registra un objeto perdido o encontrado |
| GET | `/items?estado=` | Lista los objetos según su estado |
| GET | `/items/matches?tipo=&color=` | Busca coincidencias entre perdidos y encontrados |
| PUT | `/items/<id>` | Marca un objeto perdido como recuperado |

El detalle de cada endpoint (cuerpos, respuestas y códigos de error) está en el [contrato de la API](docs/api-contract.md).