from flask import Blueprint, render_template
from app.db import db
from app.models import AIModel
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    query = """
    SELECT * FROM ai_model 
    ORDER BY download_count DESC 
    LIMIT 3
    """
    results = db.fetch_all(query)

    popular_models = []
    for row in results:
        model = AIModel(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            version=row['version'],
            license=row['license'],
            upload_date=row['upload_date'],
            update_date=row['update_date'],
            download_count=row['download_count'],
            view_count=row['view_count'],
            user_id=row['user_id'],
            torrent_file=row['torrent_file'],
            magnet_link=row['magnet_link'],
            file_size=row['file_size']
        )
        popular_models.append(model)

    return render_template('index.html', popular_models=popular_models)


@bp.route('/models')
def models():
    query = """
    SELECT m.*, GROUP_CONCAT(t.name) as tags
    FROM ai_model m
    LEFT JOIN model_tags mt ON m.id = mt.model_id
    LEFT JOIN tag t ON mt.tag_id = t.id
    GROUP BY m.id
    ORDER BY m.upload_date DESC
    """
    results = db.fetch_all(query)

    model_list = []
    for row in results:
        tags = row['tags'].split(',') if row['tags'] else []
        model = AIModel(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            version=row['version'],
            license=row['license'],
            upload_date=row['upload_date'],
            update_date=row['update_date'],
            download_count=row['download_count'],
            view_count=row['view_count'],
            user_id=row['user_id'],
            torrent_file=row['torrent_file'],
            magnet_link=row['magnet_link'],
            file_size=row['file_size'],
            tags=tags
        )
        model_list.append(model)

    return render_template('models.html', models=model_list)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/upload')
def upload():
    return render_template('upload.html')