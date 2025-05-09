from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import pymysql
from flask_login import UserMixin, LoginManager

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 设置登录视图

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime
    is_admin: bool = False

@dataclass
class AIModel:
    id: int
    name: str
    description: str
    version: str
    license: str
    upload_date: datetime
    update_date: datetime
    download_count: int
    view_count: int
    user_id: int
    username: str
    torrent_file: str
    magnet_link: Optional[str]
    model_img: str
    file_size: int
    tags: List[str] = None

@dataclass
class Tag:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

@dataclass
class ModelImage:
    id: int
    filename: str
    model_id: int
    is_primary: bool = False

class User(UserMixin):
    def __init__(self, id, username, email, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='fCfi;iKup5>N',
                                 database='ai_torrent',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE id=%s"
            cursor.execute(sql, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(id=user_data['id'],
                          username=user_data['username'],
                          email=user_data['email'],
                          is_admin=user_data['is_admin'])
    finally:
        connection.close()
    return None