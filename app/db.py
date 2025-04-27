import pymysql
from pymysql.cursors import DictCursor
from config import config


class Database:
    def __init__(self, app_config):
        self.host = app_config.MYSQL_HOST
        self.port = app_config.MYSQL_PORT
        self.user = app_config.MYSQL_USER
        self.password = app_config.MYSQL_PASSWORD
        self.db = app_config.MYSQL_DB
        self.charset = app_config.MYSQL_CHARSET
        self.conn = None

    def connect(self):
        if not self.conn or not self.conn.open:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charset,
                cursorclass=DictCursor
            )
        return self.conn

    def close(self):
        if self.conn and self.conn.open:
            self.conn.close()

    def execute(self, query, args=None):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, args or ())
            conn.commit()
            return cursor

    def fetch_one(self, query, args=None):
        with self.execute(query, args) as cursor:
            return cursor.fetchone()

    def fetch_all(self, query, args=None):
        with self.execute(query, args) as cursor:
            return cursor.fetchall()

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        with self.execute(query, tuple(data.values())) as cursor:
            return cursor.lastrowid

    def update(self, table, data, condition):
        set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        with self.execute(query, tuple(data.values())) as cursor:
            return cursor.rowcount


# 全局数据库实例
db = Database(config['default']())