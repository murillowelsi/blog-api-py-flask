from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Username or password is missing"}), 401

    # implemente a lógica de validação de credenciais aqui
    if not validate_credentials(username, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify(foo='bar'), 200


def validate_credentials(username, password):
    # implemente a lógica de validação de credenciais aqui
    return True
