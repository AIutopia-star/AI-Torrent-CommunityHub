from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class='config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # db.init_app(app)
    # migrate.init_app(app, db)

    # �޸����� - ʹ�þ��Ե���
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app