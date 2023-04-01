from flask_jwt_extended import (
    create_access_token
)

from app.repository.user_repository import UserRepository
from app.utils.util import create_error_response, create_json_response


class AuthController:
    def __init__(self, app):
        self.app = app
        self.user_repository = UserRepository()
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule(
            '/login',
            view_func=self.login,
            methods=['POST']
        )

    def login(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return create_error_response(400, 'Username is required')

        if not password:
            return create_error_response(400, 'Password is required')

        user = self.user_repository.get_user_by_username(username)

        if not user:
            return create_error_response(401, 'Invalid username or password')

        if not check_password_hash(user.password, password):
            return create_error_response(401, 'Invalid username or password')

        access_token = create_access_token(identity=user.id)
        response_data = {'access_token': access_token}
        return create_json_response(response_data, 200)
