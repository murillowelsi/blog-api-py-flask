import os
import datetime

from flasgger import swag_from
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import create_access_token
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.utils.util import create_error_response, create_json_response

base_path = '/Users/murillowelsi/PycharmProjects/blog-api/app/doc'

auth_bp = Blueprint('auth_bp', __name__)


def protected_route(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if not current_user:
            return create_error_response(401, 'Token is missing or invalid')
        return func(*args, **kwargs)

    return decorated_function


@auth_bp.route('/auth', methods=['POST'])
@swag_from(os.path.join(base_path, 'auth.yml'))
def auth_login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')

    access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=7))

    response_data = {'access_token': access_token}
    return create_json_response(response_data, 200)
