from flask import Flask, jsonify, request, render_template
from service import *


# --- Creacion de la App Flask ---
app = Flask(__name__)


# --- Endpoints ---
# Cada función es una ruta con un método HTTP
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registrar")
def registrar():
    return render_template("registrar.html")

@app.route("/listar")
def listar():
    return render_template("listar.html")

# Método GET
# Se encarga de buscar los objetos almacenados en el JSON según su estado
@app.route("/items", methods=["GET"])
def obtener_items():
    # --- Validar filtro ---

    status = request.args.get("estado")

    if status not in ("perdido", "encontrado", "recuperado"):
        return jsonify({"message": "El parámetro 'estado' es inválido"}), 400

    # --- Consultar y filtrar objetos ---

    datos = leer_archivo()

    items_filtrados = {
        id_: objeto
        for id_, objeto in datos.items()
        if objeto.get("estado") == status
    }

    return jsonify(items_filtrados), 200


# Método POST
# Crea un nuevo elemento y lo añade al archivo JSON
@app.route("/items", methods=["POST"])
def nuevo_objeto():

    data = request.get_json(silent=True)

    # --- Validar datos ---

    if not isinstance(data, dict):
        return jsonify({"message": "Los datos deben ser un JSON válido"}), 400

    campos_validos = {"tipo", "color", "fecha", "lugar", "descripcion","nombre_contacto", "numero_contacto", "estado"}

    if data.keys() != campos_validos:
        return jsonify({"message": "Se requieren todos los campos solicitados"}), 422

    if not all(isinstance(dato, str) for dato in data.values()):
        return jsonify({"message": "Todos los datos deben ser cadenas de texto."}), 422

    if not all(dato.strip() for dato in data.values()):
        return jsonify({"message": "Los campos no pueden estar vacíos"}), 422

    # --- Normalizar datos ---

    data = {
        campo: valor.strip()
        for campo, valor in data.items()
    }

    # --- Validar reglas de negocio ---

    if len(data["descripcion"]) > 200:
        return jsonify({"message": "La descripción no puede superar los 200 caracteres"}), 422

    if data["estado"] not in ("perdido", "encontrado"):
        return jsonify({"message": "El estado debe ser 'perdido' o 'encontrado'"}), 422

    if len(data["numero_contacto"]) != 10 or not data["numero_contacto"].isnumeric():
        return jsonify({"message": "El número telefónico es inválido."}), 422

    # --- Serializar objeto ---

    objeto = serializar_elemento(
        tipo=data["tipo"],
        color=data["color"],
        fecha=data["fecha"],
        lugar=data["lugar"],
        descripcion=data["descripcion"],
        nombre_contacto=data["nombre_contacto"],
        numero_contacto=data["numero_contacto"],
        estado=data["estado"]
    )

    # --- Guardar objeto ---

    try:
        nuevo_id = anadir_objeto(objeto)

    except OSError:
        return jsonify({"message": "No se pudo guardar el objeto"}), 500

    return jsonify({
        "message": "Objeto registrado correctamente",
        "id": nuevo_id,
        "item": objeto
    }), 201


# Método GET (búsqueda)
# Busca coincidencias entre objetos perdidos y encontrados por tipo y color
@app.route("/items/matches", methods=["GET"])
def buscar_coincidencias():
    # --- Validar filtros ---

    tipo = request.args.get("tipo", "").strip().casefold()
    color = request.args.get("color", "").strip().casefold()

    if not tipo or not color:
        return jsonify({"message": "Los parámetros tipo y color son obligatorios"}), 400

    # --- Consultar y filtrar objetos ---

    datos = leer_archivo()

    perdidos = {
        id_: objeto
        for id_, objeto in datos.items()
        if objeto.get("estado") == "perdido"
        and objeto.get("tipo", "").casefold() == tipo
        and objeto.get("color", "").casefold() == color
    }

    encontrados = {
        id_: objeto
        for id_, objeto in datos.items()
        if objeto.get("estado") == "encontrado"
        and objeto.get("tipo", "").casefold() == tipo
        and objeto.get("color", "").casefold() == color
    }

    # --- Relacionar perdidos con encontrados ---

    coincidencias = [
        {
            "perdido": {"id": id_perdido, **perdido},
            "encontrado": {"id": id_encontrado, **encontrado}
        }
        for id_perdido, perdido in perdidos.items()
        for id_encontrado, encontrado in encontrados.items()
    ]

    return jsonify({
        "total": len(coincidencias),
        "coincidencias": coincidencias
    }), 200


# Método PUT
# Actualiza el estado de un objeto perdido a recuperado
@app.route("/items/<int:id_>", methods=["PUT"])
def marcar_como_recuperado(id_):
    # --- Consultar objetos ---

    datos = leer_archivo()
    objeto = str(id_)

    # --- Validar reglas de negocio ---

    if objeto not in datos:
        return jsonify({"message": "No existe un objeto con ese ID"}), 404

    if datos[objeto].get("estado") != "perdido":
        return jsonify({"message": "Solo se pueden recuperar objetos perdidos"}), 409

    # --- Actualizar estado ---

    modificar_estado_a_recuperado(objeto)

    return jsonify({}), 204


# --- Ejecución de la App Flask ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)