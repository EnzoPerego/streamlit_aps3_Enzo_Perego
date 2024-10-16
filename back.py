from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@progeenzo.qvijg.mongodb.net/aps3"
mongo = PyMongo(app)

# ------------------------------------------------------------------------------
# Usuarios:

@app.route('/usuarios', methods=['GET'])
def get_all_users():
    filtro = {}
    projecao = {"_id": 0}
    dados_usuarios = mongo.db.usuarios.find(filtro, projecao)

    resp = {
        "usuarios": list(dados_usuarios)
    }

    return resp, 200

@app.route('/usuarios', methods=['POST'])
def post_user():
    data = request.json

    if "cpf" not in data:
        return {"erro": "Cpf é obrigatório"}, 400
    elif "nome_usuario" not in data:
        return {"erro": "Nome de usuario é obrigatório"}, 400
    elif "data_nascimento" not in data:
        return {"erro": "Data de nascimento é obrigatório"}, 400

    result = mongo.db.usuarios.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/usuarios/<string:id>', methods=['GET'])
def get_one_user(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    dados_usuario = mongo.db.usuarios.find_one(filtro, {"_id": 0})

    if not dados_usuario:
        return {"erro": "Usuario não encontrado"}, 404

    return {"usuario": dados_usuario}, 200

# Rota para atualizar as informações de um usuario
@app.route('/usuarios/<string:id>', methods=['PUT'])
def update_user(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    data = request.json

    result = mongo.db.usuarios.update_one(filtro, {"$set": data})

    if result.modified_count == 0:
        return {"erro": "Usuario não encontrado"}, 404

    return {"mensagem": "Usuario atualizado com sucesso!"}, 200

# Rota para deletar um usuario
@app.route('/usuarios/<string:id>', methods=['DELETE'])
def delete_user(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    result = mongo.db.usuarios.delete_one(filtro)

    if result.deleted_count == 0:
        return {"erro": "Usuario não encontrado"}, 404

    return {"mensagem": "Usuario deletado com sucesso!"}, 200

# ---------------------------------------------------------------------------

# Bikes:

@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    filtro = {}
    projecao = {"_id": 0}
    dados_bikes = mongo.db.bikes.find(filtro, projecao)

    resp = {
        "bikes": list(dados_bikes)
    }

    return resp, 200

@app.route('/bikes', methods=['POST'])
def post_bike():
    data = request.json

    if "marca" not in data:
        return {"erro": "Marca é obrigatório"}, 400
    elif "modelo" not in data:
        return {"erro": "Modelo é obrigatório"}, 400
    elif "cidade" not in data:
        return {"erro": "Cidade é obrigatório"}, 400

    data["status"] = "disponivel"
    result = mongo.db.bikes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/bikes/<string:id>', methods=['GET'])
def get_one_bike(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    dados_bike = mongo.db.bikes.find_one(filtro, {"_id": 0})

    if not dados_bike:
        return {"erro": "Bike não encontrada"}, 404

    return {"bike": dados_bike}, 200

# Rota para atualizar as informações de uma bike
@app.route('/bikes/<string:id>', methods=['PUT'])
def update_bike(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    data = request.json

    result = mongo.db.bikes.update_one(filtro, {"$set": data})

    if result.modified_count == 0:
        return {"erro": "Bike não encontrada"}, 404

    return {"mensagem": "Bike atualizada com sucesso!"}, 200

# Rota para deletar uma bike
@app.route('/bikes/<string:id>', methods=['DELETE'])
def delete_bike(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    result = mongo.db.bikes.delete_one(filtro)

    if result.deleted_count == 0:
        return {"erro": "Bike não encontrada"}, 404

    return {"mensagem": "Bike deletada com sucesso!"}, 200

# -------------------------------------------------------------------------------------------

# Empréstimos:

@app.route('/emprestimos', methods=['GET'])
def get_all_emprestimos():
    emprestimos = mongo.db.emprestimos.find()
    resultado = []

    for emprestimo in emprestimos:
        resultado.append({
            "id": str(emprestimo["_id"]),
            "id_usuario": str(emprestimo["id_usuario"]),
            "bike_id": str(emprestimo["id_bike"]),
            "data_emprestimo": emprestimo["data_emprestimo"]
        })

    return jsonify(resultado), 200

@app.route('/emprestimos/usuarios/<string:id_usuario>/bikes/<string:id_bike>', methods=['POST'])
def post_emprestimo(id_usuario, id_bike):
    usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        return {"erro": "Usuario nao encontrado."}, 404
    
    bike = mongo.db.bikes.find_one({"_id": ObjectId(id_bike)})
    if not bike:
        return {"erro": "Bike nao encontrada."}, 404

    # Verificar se a bike já está em uso
    emprestimo_ativo = mongo.db.emprestimos.find_one({"id_bike": ObjectId(id_bike), "status": "ativo"})
    if emprestimo_ativo:
        return {"message": "Bike esta em uso."}, 400

    novo_emprestimo = {
        "id_bike": ObjectId(id_bike),
        "id_usuario": ObjectId(id_usuario),
        "status": "ativo",
        "data_emprestimo": datetime.now()  # A data de empréstimo é registrada automaticamente
    }

    result = mongo.db.emprestimos.insert_one(novo_emprestimo)

    mongo.db.bikes.update_one({"_id": ObjectId(id_bike)}, {"$set": {"status": "em uso"}})

    return {
        "id": str(result.inserted_id),
        "message": "Empréstimo realizado com sucesso!"
    }, 201

@app.route('/emprestimos/<string:id_emprestimo>', methods=['DELETE'])
def delete_emprestimo(id_emprestimo):
    emprestimo = mongo.db.emprestimos.find_one({"_id": ObjectId(id_emprestimo)})
    
    if not emprestimo:
        return {"erro": "Empréstimo não encontrado"}, 404
    
    id_bike = emprestimo.get("id_bike")
    if not id_bike:
        return {"erro": "Bike não encontrada"}, 404
    
    mongo.db.bikes.update_one({"_id": id_bike}, {"$set": {"status": "disponível"}})
    
    mongo.db.emprestimos.delete_one({"_id": ObjectId(id_emprestimo)})
    
    return {"message": "Empréstimo deletado"}, 200

if __name__ == '__main__':
    app.run(debug=True)
