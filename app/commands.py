import click
from app import db
from app.models import User, AIModel, Tag
from datetime import datetime

@click.command('init-db')
def init_db():
    """清空并重建数据库"""
    db.drop_all()
    db.create_all()
    click.echo('数据库已初始化')

def init_db_command():
    """初始化数据库命令"""
    return init_db


def init_db_command():
    """初始化数据库命令"""

    @click.command('init-db')
    def init_db():
        """清空并重建数据库，并添加示例数据"""
        click.echo('正在初始化数据库...')
        db.drop_all()
        db.create_all()

        # 添加示例数据
        click.echo('添加示例数据...')

        # 添加测试用户
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash='pbkdf2:sha256:260000$...'  # 实际使用时应该生成真实hash
        )
        db.session.add(admin)

        # 添加一些标签
        tags = ['Stable Diffusion', 'Anime', 'Photorealistic', 'NSFW', 'Landscape']
        for tag_name in tags:
            db.session.add(Tag(name=tag_name))

        # 添加示例模型
        example_model = AIModel(
            name="Stable Diffusion 2.1",
            description="Example AI model for testing",
            version="2.1",
            license="MIT",
            upload_date=datetime.utcnow(),
            download_count=0,
            user_id=1,
            torrent_file="models/stable-diffusion-2.1.torrent",
            file_size=1024 * 1024 * 1024 * 4  # 4GB
        )
        db.session.add(example_model)

        db.session.commit()
        click.echo('数据库初始化完成')

    return init_db