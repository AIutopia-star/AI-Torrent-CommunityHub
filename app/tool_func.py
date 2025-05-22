import hashlib
import os

import bencode
import pymysql


def generate_magnet_link(torrent_file_path):
    # 读取种子文件
    with open(torrent_file_path, 'rb') as f:
        torrent_data = f.read()

    # 解码种子文件
    torrent_info = bencode.bdecode(torrent_data)
    info_hash = hashlib.sha1(bencode.bencode(torrent_info['info'])).hexdigest()

    # 生成磁力链接
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}"
    return magnet_link

# 数据库连接配置
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='fCfi;iKup5>N',
        database='ai_torrent',
        cursorclass=pymysql.cursors.DictCursor
    )
