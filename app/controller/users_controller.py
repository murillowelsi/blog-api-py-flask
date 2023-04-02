import os

from flasgger import swag_from
from flask import Blueprint, request

from app.controller.auth_controller import protected_route
from app.service.user_service import UserService
from app.utils.util import create_json_response, create_error_response

base_path = '/Users/murillowelsi/PycharmProjects/blog-api/app/doc'

users_bp = Blueprint('users_bp', __name__)
user_service = UserService()


@users_bp.before_request
@protected_route
def before_request():
    pass


@users_bp.route('/users', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_all_users.yml'))
def get_all_users():
    sort_by = request.args.get('sort', 'id')
    sort_column = 'created_at' if sort_by == 'created_at' else 'id'

    users = user_service.get_all_users(sort_by=sort_column)

    response_data = users

    if sort_column == 'created_at':
        response_data = sorted(response_data, key=lambda k: k['created_at'])

    return create_json_response(response_data, 200)


@users_bp.route('/users/<int:id>', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_users_by_id.yml'))
def get_post_by_id(id):
    user = user_service.get_user_by_id(id)

    if user is None:
        return create_error_response(404, 'User not found')

    formatted_user = user
    return create_json_response(formatted_user, 200)


@users_bp.route('/users', methods=['POST'])
@swag_from(os.path.join(base_path, 'create_user.yml'))
def create_user():
    data = request.get_json()
    username, password, email = data.get('username'), data.get('password'), data.get('email')

    user = user_service.create_user(username=username, password=password, email=email)

    response_data = user
    return create_json_response(response_data, 201)


@users_bp.route('/users/<int:id>', methods=['DELETE'])
@swag_from(os.path.join(base_path, 'delete_user_by_id.yml'))
def delete_user_by_id(id):
    success = user_service.delete_user_by_id(id)

    if success:
        return create_json_response({}, 204)
    else:
        return create_error_response(404, 'User not found')


@users_bp.route('/users/<int:id>', methods=['PUT'])
@swag_from(os.path.join(base_path, 'update_user_by_id.yml'))
def update_post_by_id(id):
    data = request.get_json()
    username, password, email = data.get('username'), data.get('password'), data.get('email')

    updated_user = user_service.update_user_by_id(id, username=username, password=password, email=email)

    if updated_user is None:
        return create_error_response(404, 'User not found')

    response_data = updated_user
    return create_json_response(response_data, 200)
