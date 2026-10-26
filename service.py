"""Módulo que contiene la lógica de negocio de la app"""

from json import dump, load, JSONDecodeError

# Constante con la ruta al archivo JSON que contiene los objetos almacenados
LISTA_OBJETOS = "data/objetos.json"


def serializar_elemento(
        tipo: str,
        color: str,
        fecha: str,
        lugar: str,
        descripcion: str,
        nombre_contacto: str,
        numero_contacto: str,
        estado: str) -> dict:
    """Serializa un objeto en un diccionario

    Args:
        tipo (str): Tipo del objeto
        color (str): Color del objeto
        fecha (str): Fecha en que se perdió/encontró
        lugar (str): Lugar aproximado donde ocurrió el evento
        descripcion (str): Descripción corta del objeto (max 200 caracteres)
        nombre_contacto (str): Nombre de la persona que registró el evento
        numero_contacto (str): Número de contacto de la persona que registró el evento
        estado (str): Estado del objeto (perdido/encontrado/recuperado)

    Returns:
        dict: Diccionario con los datos del objeto
    """

    return {
        "tipo": tipo,
        "color": color,
        "fecha": fecha,
        "lugar": lugar,
        "descripcion": descripcion,
        "nombre_contacto": nombre_contacto,
        "numero_contacto": numero_contacto,
        "estado": estado
    }


def generar_id(objetos: dict) -> int:
    """Genera un ID nuevo para almacenar un nuevo objeto

    Args:
        objetos (dict): El diccionario con los objetos actuales

    Returns:
        int: El ID nuevo
    """

    return max(
        (int(id_) for id_ in objetos.keys()),
        default=0
    ) + 1


def leer_archivo() -> dict:
    """Carga los datos almacenados en el JSON

    Returns:
        dict: Un diccionario con los objetos almacenados
    """

    try:
        with open(LISTA_OBJETOS, "r", encoding="utf-8") as archivo:
            return load(archivo)

    except (FileNotFoundError, JSONDecodeError):
        return {}


def guardar_archivo(datos: dict):
    """Guarda los cambios en el archivo JSON

    Args:
        datos (dict): El diccionario con los datos actualizados
    """

    with open(LISTA_OBJETOS, "w", encoding="utf-8") as archivo:
        dump(datos, archivo, indent=4, ensure_ascii=False)


def anadir_objeto(objeto: dict) -> str:
    """Añade un objeto nuevo al archivo JSON

    Args:
        objeto (dict): El nuevo objeto a añadir

    Returns:
        str: El ID del nuevo objeto
    """

    datos = leer_archivo()
    nuevo_id = str(generar_id(datos))

    datos[nuevo_id] = objeto

    guardar_archivo(datos)

    return nuevo_id


def modificar_estado_a_recuperado(id_objeto: str):
    """Modifica el estado de un objeto perdido a recuperado

    Args:
        id_objeto (str): El ID del objeto a modificar
    """

    datos = leer_archivo()
    datos[id_objeto]["estado"] = "recuperado"

    guardar_archivo(datos)