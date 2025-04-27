from flask import Flask
from .db import db
from config import config


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化数据库连接
    @app.before_request
    def before_request():
        db.connect()

    @app.teardown_request
    def teardown_request(exception):
        db.close()

    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app