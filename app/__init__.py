from flask import Flask
from .db import db
from config import config
from flask_login import LoginManager
from app.routes import auth
from app.routes import user



def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
    # 初始化扩展
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # 初始化数据库连接
    @app.before_request
    def before_request():
        db.connect()

    @app.teardown_request
    def teardown_request(exception=None):
        if db and db.conn and db.conn.open:
            db.close()

    @login_manager.user_loader
    def load_user(user_id):
        # 你的用户加载逻辑
        pass
    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app