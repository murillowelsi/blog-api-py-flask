from flasgger import Swagger
from flask_migrate import Migrate

from app import create_app
from app.controller.auth_controller import AuthController
from app.controller.posts_controller import posts_bp
from app.controller.users_controller import users_bp
from app.database import create_tables
from app.database import db

app = create_app()
auth_controller = AuthController(app)

create_tables(app)

app.register_blueprint(posts_bp)
app.register_blueprint(users_bp)

migrate = Migrate(app, db)
app.config['SWAGGER'] = {
    'title': 'Blog API - By Murillo Welsi',
    'uiversion': 3
}
swagger = Swagger(app)

if __name__ == '__main__':
    app.run()
