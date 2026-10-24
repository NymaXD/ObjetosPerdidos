from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = {}


@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    keys = ["nombre", "email", "password"]

    if not list(data.keys()) == keys:
        return jsonify({
            "message": "Faltan datos"
        }), 400

    for u in usuarios.values():
        if data["email"] == u["email"]:
            return "Email ya se encuentra registrado", 409

    id_ = len(usuarios) + 1
    
    usuarios[id_] = data

    return jsonify({
        "message": "Usuario creado",
        "name": data["nombre"]
    }), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(usuarios), 200


@app.route("/users/<int:id_>", methods=["PATCH"])
def change_password(id_):

    data = request.get_json()

    if len(data) != 1 or list(data.keys()) != ["password"]:
        return jsonify({
            "message": "Bad request"
        }), 400

    if id_ in usuarios.keys():
        usuarios[id_].update(data)

        return jsonify({
            "message": "Contraseña modificada correctamente"
        }), 200

    else:
        return jsonify({
            "message": "Usuario no existente"
        }), 404

if __name__ == "__main__":
    app.run(debug=True)
