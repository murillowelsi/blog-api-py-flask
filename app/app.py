from flask_migrate import Migrate
from app.database import db
from app.routes.posts_route import bp
from app import create_app
from app.database import create_tables
from flasgger import Swagger

app = create_app()

create_tables(app)

app.register_blueprint(bp)
migrate = Migrate(app, db)
swagger = Swagger(app)

if __name__ == '__main__':
    app.run()
