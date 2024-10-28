from flask import Flask
from db_setup import db  # Import the db instance
from flask_migrate import Migrate

# Initialize Migrate instance
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration for MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/lab4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to create tables
    with app.app_context():
        from .models import City, Person  # Import your models here

    # Register Blueprints
    from app.controllers.user_controller import user_controller
    from app.controllers.city_controller import city_controller
    app.register_blueprint(user_controller)
    app.register_blueprint(city_controller)

    @app.route('/')
    def index():
        return "Hello, World!"

    return app

# Entry point for running the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
