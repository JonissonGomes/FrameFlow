from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import datetime

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "Dados inválidos"}), 400

    mongo = current_app.mongo
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "Usuário já existe"}), 400

    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.datetime.utcnow()
    }
    mongo.db.users.insert_one(user)
    
    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Dados inválidos"}), 400

    mongo = current_app.mongo
    user = mongo.db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({"access_token": access_token}), 200