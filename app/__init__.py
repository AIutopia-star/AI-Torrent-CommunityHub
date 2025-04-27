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

    # 修改这里 - 使用绝对导入
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app