import pymysql
from datetime import datetime, timedelta
from config import config
import random

# 连接数据库
conn = pymysql.connect(
    host=config['default']().MYSQL_HOST,
    port=config['default']().MYSQL_PORT,
    user=config['default']().MYSQL_USER,
    password=config['default']().MYSQL_PASSWORD,
    db=config['default']().MYSQL_DB,
    charset=config['default']().MYSQL_CHARSET
)


def insert_sample_data():
    try:
        with conn.cursor() as cursor:
            # 清空现有数据
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE user")
            cursor.execute("TRUNCATE TABLE tag")
            cursor.execute("TRUNCATE TABLE ai_model")
            cursor.execute("TRUNCATE TABLE model_tags")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # 插入测试用户
            cursor.execute("""
            INSERT INTO user (username, email, password_hash, created_at, is_admin)
            VALUES (%s, %s, %s, %s, %s)
            """, ('admin', 'admin@aimodelshare.com', 'hashed_password', datetime.now(), True))

            user_id = cursor.lastrowid

            # 插入标签
            tags = ['Stable Diffusion', 'Anime', 'Photorealistic', 'NSFW', 'Landscape',
                    'Portrait', 'Fantasy', 'Sci-Fi', 'Cyberpunk', 'Watercolor']
            tag_ids = {}

            for tag in tags:
                cursor.execute("INSERT INTO tag (name) VALUES (%s)", (tag,))
                tag_ids[tag] = cursor.lastrowid

            # 插入AI模型
            models = [
                {
                    'name': 'Stable Diffusion 2.1',
                    'description': 'Latest stable version of Stable Diffusion model',
                    'version': '2.1',
                    'license': 'CreativeML Open RAIL-M',
                    'file_size': 4300000000,
                    'tags': ['Stable Diffusion', 'Photorealistic']
                },
                {
                    'name': 'Anime Diffusion',
                    'description': 'Specialized model for anime-style artwork',
                    'version': '1.5',
                    'license': 'MIT',
                    'file_size': 3800000000,
                    'tags': ['Anime', 'Fantasy']
                },
                {
                    'name': 'Cyberpunk Neon',
                    'description': 'Cyberpunk and neon light style generator',
                    'version': '3.0',
                    'license': 'CC BY-NC 4.0',
                    'file_size': 4100000000,
                    'tags': ['Cyberpunk', 'Sci-Fi']
                },
                {
                    'name': 'Watercolor Dreams',
                    'description': 'Beautiful watercolor painting style',
                    'version': '1.2',
                    'license': 'Apache 2.0',
                    'file_size': 3500000000,
                    'tags': ['Watercolor', 'Landscape', 'Portrait']
                },
                {
                    'name': 'Fantasy Portrait Pro',
                    'description': 'Professional fantasy portrait generator',
                    'version': '2.3',
                    'license': 'CC BY 4.0',
                    'file_size': 3900000000,
                    'tags': ['Fantasy', 'Portrait']
                }
            ]

            for model in models:
                upload_date = datetime.now() - timedelta(days=random.randint(1, 30))
                cursor.execute("""
                INSERT INTO ai_model 
                (name, description, version, license, upload_date, update_date, 
                 download_count, view_count, user_id, torrent_file, file_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    model['name'],
                    model['description'],
                    model['version'],
                    model['license'],
                    upload_date,
                    upload_date,
                    random.randint(100, 5000),
                    random.randint(500, 10000),
                    user_id,
                    f"torrents/{model['name'].lower().replace(' ', '-')}.torrent",
                    model['file_size']
                ))

                model_id = cursor.lastrowid

                # 插入模型标签关联
                for tag in model['tags']:
                    cursor.execute("""
                    INSERT INTO model_tags (model_id, tag_id)
                    VALUES (%s, %s)
                    """, (model_id, tag_ids[tag]))

            conn.commit()
            print("成功插入示例数据！")

    finally:
        conn.close()


if __name__ == '__main__':
    insert_sample_data()