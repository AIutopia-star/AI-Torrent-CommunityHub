from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/models')
def models():
    return render_template('models.html')

@bp.route('/upload')
def upload():
    return render_template('upload.html')