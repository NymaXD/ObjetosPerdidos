# Contrato de API: Objetos perdidos y encontrados

Versión 1.1 · Backend Flask · Para el equipo de frontend

## Generalidades

- **URL base (desarrollo):** `http://127.0.0.1:5000`
- **Formato:** las peticiones con cuerpo y las respuestas con contenido son JSON (`Content-Type: application/json`). Una respuesta 204 no tiene body.
- **Autenticación:** ninguna.
- **IDs:** siempre `string` (por ejemplo `"1"`).
- **Errores:** siempre tienen la forma `{ "message": "texto del error" }`.
- **CORS:** habilitado para cualquier origen, así que el navegador permite llamar a la API desde otro origen (por ejemplo `localhost:5500` o `localhost:5173`) sin configuración adicional en el frontend.

## Modelo: Objeto

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `tipo` | string | Tipo del objeto (ej. "Billetera") |
| `color` | string | Color del objeto |
| `fecha` | string | Fecha en que se perdió o encontró. El formato no se valida; se recomienda `AAAA-MM-DD` |
| `lugar` | string | Lugar aproximado del evento |
| `descripcion` | string | Descripción corta, máximo 200 caracteres |
| `nombre_contacto` | string | Nombre de quien registra |
| `numero_contacto` | string | Celular de contacto de quien registra: exactamente 10 dígitos numéricos (ej. 3001234567) |
| `estado` | string | `perdido`, `encontrado` o `recuperado` |

Todos los campos son obligatorios, no pueden estar vacíos y el backend les quita los espacios al inicio y al final.

## Endpoints

### 1. Registrar un objeto

`POST /items`

**Body** (los 8 campos, ni más ni menos):

```json
{
  "tipo": "Billetera",
  "color": "Negro",
  "fecha": "2026-10-01",
  "lugar": "Biblioteca",
  "descripcion": "Cuero",
  "nombre_contacto": "Ana",
  "numero_contacto": "3001234567",
  "estado": "perdido"
}
```

Al registrar, `estado` solo puede ser `perdido` o `encontrado`. El valor `recuperado` se asigna únicamente con el endpoint 4.

**Respuestas:**

| Código | Cuándo | Body |
| --- | --- | --- |
| 201 | Objeto creado | `{ "message": "Objeto registrado correctamente", "id": "1", "item": { ...Objeto } }` |
| 400 | El body no es un JSON válido | `{ "message": "Los datos deben ser un JSON válido" }` |
| 422 | Faltan o sobran campos, algún valor no es string, hay campos vacíos, la descripción supera 200 caracteres, el número de contacto no tiene exactamente 10 dígitos numéricos o el estado no es `perdido`/`encontrado` | `{ "message": "..." }` |
| 500 | Error al guardar en el servidor | `{ "message": "No se pudo guardar el objeto" }` |

### 2. Listar objetos por estado

`GET /items?estado={estado}`

- `estado` es obligatorio y debe ser `perdido`, `encontrado` o `recuperado`.

**Respuestas:**

| Código | Cuándo | Body |
| --- | --- | --- |
| 200 | Filtro válido | Objeto indexado por ID (ver ejemplo). Si no hay resultados, `{}` |
| 400 | `estado` ausente o inválido | `{ "message": "El parámetro 'estado' es inválido" }` |

**Ejemplo 200:**

```json
{
  "1": {
    "tipo": "Billetera",
    "color": "Negro",
    "fecha": "2026-10-01",
    "lugar": "Biblioteca",
    "descripcion": "Cuero",
    "nombre_contacto": "Ana",
    "numero_contacto": "3001234567",
    "estado": "perdido"
  }
}
```

La respuesta es un **objeto indexado por ID**, no un arreglo. Para recorrerla en JavaScript: `Object.entries(data)`.

### 3. Buscar coincidencias

`GET /items/matches?tipo={tipo}&color={color}`

- `tipo` y `color` son obligatorios.
- La comparación ignora mayúsculas y espacios en los extremos, pero exige igualdad exacta ("Billetera" coincide con "billetera", no con "cartera").
- Devuelve todas las parejas posibles entre objetos `perdido` y `encontrado` con ese tipo y color.

**Respuestas:**

| Código | Cuándo | Body |
| --- | --- | --- |
| 200 | Filtros válidos | `{ "total": n, "coincidencias": [ ... ] }`. Sin coincidencias: `total: 0` y arreglo vacío |
| 400 | Falta `tipo` o `color` | `{ "message": "Los parámetros tipo y color son obligatorios" }` |

**Ejemplo 200:**

```json
{
  "total": 1,
  "coincidencias": [
    {
      "perdido": { "id": "1", "tipo": "Billetera", "color": "Negro", "estado": "perdido", "...": "..." },
      "encontrado": { "id": "2", "tipo": "billetera", "color": "negro", "estado": "encontrado", "...": "..." }
    }
  ]
}
```

En este endpoint cada objeto incluye su `id` dentro del propio objeto (los "..." representan el resto de campos del modelo).

### 4. Marcar un objeto como recuperado

`PUT /items/{id}`

- No lleva body, y la respuesta exitosa tampoco (204): el frontend no debe llamar a response.json() en ella.
- `{id}` debe ser un entero (ej. `/items/1`).
- Solo se puede aplicar a objetos en estado `perdido`.

**Respuestas:**

| Código | Cuándo | Body |
| --- | --- | --- |
| 204 | Objeto actualizado | Sin body (respuesta vacía) |
| 404 | No existe un objeto con ese ID | `{ "message": "No existe un objeto con ese ID" }` |
| 409 | El objeto no está en estado `perdido` (incluye repetir el PUT) | `{ "message": "Solo se pueden recuperar objetos perdidos" }` |

## Resumen de códigos de estado

| Código | Significado en esta API |
| --- | --- |
| 200 | Operación exitosa |
| 201 | Objeto creado |
| 204 | Operación exitosa sin body (PUT) |
| 400 | Petición mal formada (JSON inválido o parámetro de consulta ausente/inválido) |
| 404 | El ID no existe |
| 409 | Conflicto de estado (el objeto no está perdido) |
| 422 | El JSON es válido pero los datos no cumplen las reglas |
| 500 | Error del servidor al guardar |
