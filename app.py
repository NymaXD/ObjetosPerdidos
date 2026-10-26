from flask import Flask, jsonify, request

# --- Creacion de la App Flask ---
app = Flask(__name__)


# --- Endpoints ---
# Cada función es una ruta con un método HTTP

# Método GET
# Se encarga de buscar los objetos almacenados en el JSON según el estado 'perdido' o 'encontrado'
@app.route("/items", methods=["GET"])
def obtener_items():
    status = request.args.get("status")

    if status not in ("lost", "found"):
        return jsonify({
            "error": "Indica status=lost o status=found"
        }), 400

    # Consultar la base de datos según el estado.
    return jsonify({"status": status}), 200


# Método POST
# Crea un nuevo elemento y lo añade al archivo JSON
@app.route("/items", methods=["POST"])
def nuevo_objeto():
    return jsonify({"message": "Endpoint funcionando"}), 200


# Método GET (búsqueda)
# Busca las coincidencias de objetos perdidos y encontrados mediante filtros
@app.route("/items/matches", methods=["GET"])
def buscar_coincidencias():
    tipo = request.args.get("tipo")
    color = request.args.get("color")

    if not tipo or not color:
        return jsonify({
            "error": "Los parámetros tipo y color son obligatorios"
        }), 400

    # 1. Buscar objetos perdidos del tipo y color indicados.
    # 2. Buscar objetos encontrados con esas características.
    # 3. Relacionar los resultados y devolver las coincidencias.

    return jsonify({"message": "endpoint funcionando"}), 200


# Método PUT
# Actualiza el estado de un objeto de 'perdido' a 'encontrado'
@app.route("/lost_items/<int:id_>", methods=["PUT"])
def marcar_como_recuperado(id_):
    return jsonify({"message": "Endpoint funcionando"}), 200


# --- Ejecución de la App Flask ---
if __name__ == "__main__":
    app.run(debug=True)
