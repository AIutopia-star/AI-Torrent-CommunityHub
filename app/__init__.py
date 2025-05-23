import os
from datetime import timedelta

from flask import Flask
from .db import db
from config import config
from flask_login import LoginManager
from app.routes import auth
from app.routes import user
from .models import User


def create_app(config_name='default'):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])
    app.secret_key = '123456789JJKKLLLKKKKK'  # 应该是一个随机字符串
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app\\static\\uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # 初始化扩展
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = "strong"  # 安全保护级别
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(days=7)  # 设置有效期

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
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
        user = User.load_user(user_id)
        return user

    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app