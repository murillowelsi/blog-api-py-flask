from flasgger import Swagger
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate

from app import create_app
from app.controller.auth_controller import auth_bp
from app.controller.posts_controller import posts_bp
from app.controller.users_controller import users_bp
from app.database import create_tables
from app.database import db

app = create_app()

create_tables(app)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)


@jwt.expired_token_loader
def handle_expired_token_callback(expired_token):
    return jsonify({"message": "Your token has expired."}), 401


@jwt.invalid_token_loader
def handle_invalid_token_callback(invalid_token):
    return jsonify({"message": "Invalid token. Please log in again."}), 401


@app.errorhandler(JWTExtendedException)
def handle_jwt_error(exception):
    return jsonify({"message": str(exception)}), 401


migrate = Migrate(app, db)
app.config['SWAGGER'] = {
    'title': 'Blog API - By Murillo Welsi',
    'uiversion': 3
}
swagger = Swagger(app)

if __name__ == '__main__':
    app.run()
