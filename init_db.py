import pymysql
from config import config


def init_database():
    cfg = config['default']()

    # 连接MySQL服务器(不指定数据库)
    conn = pymysql.connect(
        host=cfg.MYSQL_HOST,
        port=cfg.MYSQL_PORT,
        user=cfg.MYSQL_USER,
        password=cfg.MYSQL_PASSWORD,
        charset=cfg.MYSQL_CHARSET
    )

    try:
        with conn.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cfg.MYSQL_DB} CHARACTER SET {cfg.MYSQL_CHARSET}")

            # 切换到新数据库
            cursor.execute(f"USE {cfg.MYSQL_DB}")

            # 创建表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(64) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL,
                created_at DATETIME NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                INDEX idx_username (username),
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_model (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                version VARCHAR(20),
                license VARCHAR(50),
                upload_date DATETIME NOT NULL,
                update_date DATETIME NOT NULL,
                download_count INT DEFAULT 0,
                view_count INT DEFAULT 0,
                user_id INT NOT NULL,
                torrent_file VARCHAR(200) NOT NULL,
                magnet_link VARCHAR(500),
                file_size BIGINT,
                FOREIGN KEY (user_id) REFERENCES user(id),
                INDEX idx_name (name),
                INDEX idx_upload_date (upload_date),
                INDEX idx_download_count (download_count)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            # 创建其他表...

        conn.commit()
        print("数据库初始化成功")
    finally:
        conn.close()


if __name__ == '__main__':
    init_database()