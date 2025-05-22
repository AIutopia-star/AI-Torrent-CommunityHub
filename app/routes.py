import uuid
from datetime import datetime
import os
from math import ceil
from flask import Blueprint, render_template, request, abort, redirect, url_for, flash, jsonify, session, current_app
from werkzeug.utils import secure_filename
from app.db import db
from app.models import AIModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import pymysql.cursors
from .forms import LoginForm, RegistrationForm, ModelUploadForm
from .tool_func import generate_magnet_link, get_db_connection

bp = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
user = Blueprint('user', __name__)


@bp.route('/')
def index():
    login_form = LoginForm()
    register_form = RegistrationForm()
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
            username=row['username'],
            torrent_file=row['torrent_file'],
            magnet_link=row['magnet_link'],
            model_img=row['model_img'],
            file_size=row['file_size']
        )
        popular_models.append(model)

    return render_template('index.html',
                           popular_models=popular_models,
                           login_form=login_form,
                           register_form=register_form)


@bp.route('/models')
def models():
    login_form = LoginForm()
    register_form = RegistrationForm()
    page = request.args.get('page', 1, type=int)
    per_page = 9
    search_query = request.args.get('q', '').strip()
    tag_filter = request.args.get('tag')
    sort_method = request.args.get('sort', 'newest')

    # 基础查询
    query = """
    SELECT m.*, GROUP_CONCAT(t.name) as tags, u.username
    FROM ai_model m
    LEFT JOIN model_tags mt ON m.id = mt.model_id
    LEFT JOIN tag t ON mt.tag_id = t.id
    LEFT JOIN user u ON m.user_id = u.id
    """

    # 添加WHERE条件
    conditions = []
    params = []

    if search_query:
        conditions.append("(m.name LIKE %s OR m.description LIKE %s)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if tag_filter:
        conditions.append("t.name = %s")
        params.append(tag_filter)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # 添加GROUP BY
    query += " GROUP BY m.id"

    # 添加排序
    if sort_method == 'popular':
        query += " ORDER BY m.view_count DESC"
    elif sort_method == 'downloads':
        query += " ORDER BY m.download_count DESC"
    else:  # newest
        query += " ORDER BY m.upload_date DESC"

    # 获取所有标签用于筛选
    all_tags = db.fetch_all("SELECT name FROM tag ORDER BY name")

    # 执行查询
    results = db.fetch_all(query, params)

    # 分页处理
    total_models = len(results)
    total_pages = ceil(total_models / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_results = results[start_idx:end_idx]

    # 转换为模型对象
    models = []
    for row in paginated_results:
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
            username=row['username'],
            torrent_file=row['torrent_file'],
            magnet_link=row['magnet_link'],
            model_img=row['model_img'],
            file_size=row['file_size'],
            tags=tags
        )
        models.append(model)

    # 传递给模板的分页对象
    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total_models,
        'pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'iter_pages': lambda: range(1, total_pages + 1)
    }

    return render_template(
        'models.html',
        models=models,
        all_tags=all_tags,
        pagination=pagination,
        login_form=login_form,
        register_form=register_form
    )


@bp.route('/model/<int:model_id>')
def model_detail(model_id):
    login_form = LoginForm()
    register_form = RegistrationForm()
    # 获取模型详情
    query = """
    SELECT m.*, GROUP_CONCAT(t.name) as tags, u.username
    FROM ai_model m
    LEFT JOIN model_tags mt ON m.id = mt.model_id
    LEFT JOIN tag t ON mt.tag_id = t.id
    LEFT JOIN user u ON m.user_id = u.id
    WHERE m.id = %s
    GROUP BY m.id
    """
    row = db.fetch_one(query, (model_id,))

    if not row:
        abort(404)

    # 增加查看计数
    db.execute("UPDATE ai_model SET view_count = view_count + 1 WHERE id = %s", (model_id,))

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
        username=row['username'],
        torrent_file=row['torrent_file'],
        magnet_link=row['magnet_link'],
        model_img=row['model_img'],
        file_size=row['file_size'],
        tags=tags
    )

    return render_template('model_detail.html',
                           model=model,
                           login_form=login_form,
                           register_form=register_form)


@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/upload_model')
def upload_model():
    return render_template('upload.html')


@bp.route('/upload')
def upload():
    return render_template('upload.html')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user WHERE email=%s"
                cursor.execute(sql, (email,))
                user_data = cursor.fetchone()

                if user_data and check_password_hash(user_data['password_hash'], password):
                    from app.models import User  # 延迟导入避免循环引用
                    user = User(id=user_data['id'],
                                username=user_data['username'],
                                email=user_data['email'],
                                is_admin=user_data['is_admin'])
                    login_user(user, remember=form.remember.data)
                    session.permanent = True  # 使会话持久化
                    print(f"Loaded user: {user_data}")
                    return jsonify({
                        'success': True,
                        'user': {
                            'username': user.username,
                            'is_admin': user.is_admin
                        }})
                else:
                    return jsonify({'success': False, 'errors': {'email': ['Invalid email or password']}})
        finally:
            connection.close()
    return jsonify({'success': False, 'errors': form.errors})


@auth.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("提交注册")
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                print("插入用户数据")
                try:
                    print("插入用户数据")
                    sql = """INSERT INTO user (username, email, password_hash, created_at, is_admin) 
                              VALUES (%s, %s, %s, NOW(), %s)"""
                    cursor.execute(sql, (username, email, password, False))
                    connection.commit()
                    print("用户数据插入成功")
                except Exception as e:
                    connection.rollback()
                    print(f"用户数据插入失败: {e}")

                # 自动登录新注册用户
                sql = "SELECT * FROM user WHERE email=%s"
                cursor.execute(sql, (email,))
                user_data = cursor.fetchone()
                from app.models import User
                user = User(id=user_data['id'],
                            username=user_data['username'],
                            email=user_data['email'],
                            is_admin=user_data['is_admin'])
                login_user(user)
                return jsonify({
                    'success': True,
                    'user': {
                        'username': user.username,
                        'is_admin': user.is_admin
                    }})
        except Exception as e:
            connection.rollback()
            return jsonify({'success': False, 'errors': {'database': ['Registration failed. Please try again.']}})
        finally:
            connection.close()
    return jsonify({'success': False, 'errors': form.errors})


@auth.route('/logout')
def logout():
    print("登出")
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))


@user.route('/profile')
@login_required
def profile():
    login_form = LoginForm()
    register_form = RegistrationForm()
    form = ModelUploadForm()
    print(f"Current user: {current_user}")
    return render_template('user/profile.html', user=current_user,
                           login_form=login_form,
                           register_form=register_form, form=form)

@user.route('/upload_model', methods=['POST'])
def upload_model():
    form = ModelUploadForm()
    if form.validate_on_submit():
        # 获取表单数据
        # id = str(uuid.uuid4())
        name = form.name.data
        description = form.description.data
        version = form.version.data
        license = form.license.data
        tags = form.tags.data.split(',') if form.tags.data else []
        torrent_file = form.torrent_file.data

        is_private = form.is_private.data

        # 获取当前用户信息
        user_id = current_user.id
        username = current_user.username

        # 保存种子文件和图片到服务器
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_upload_folder = os.path.join(upload_folder, str(user_id))
        os.makedirs(user_upload_folder, exist_ok=True)

        # 创建种子文件和图片文件夹
        torrent_folder = os.path.join(user_upload_folder, 'torrents')
        image_folder = os.path.join(user_upload_folder, 'images')
        os.makedirs(torrent_folder, exist_ok=True)
        os.makedirs(image_folder, exist_ok=True)

        # 保存种子文件
        filename = secure_filename(torrent_file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        torrent_file_path = os.path.join(torrent_folder, filename)
        torrent_file.save(torrent_file_path)

        # 保存图片文件（如果有的话）
        model_img = form.model_img.data
        if model_img:
            img_filename = secure_filename(model_img.filename)
            img_timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            img_filename = f"{img_timestamp}_{img_filename}"
            model_img_path = os.path.join(image_folder, img_filename)
            model_img.save(model_img_path)
        else:
            model_img_path = 'default_model_img.jpg'  # 默认图片路径

        # 生成系统字段
        upload_date = datetime.utcnow()
        update_date = datetime.utcnow()
        download_count = 0
        view_count = 0
        file_size = os.path.getsize(torrent_file_path) # 假设文件已经保存到服务器
        model_img = model_img_path  # 默认图片或用户上传的图片路径
        magnet_link = generate_magnet_link(torrent_file_path)  # 假设有一个函数生成磁力链接

        # 插入数据到数据库
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO ai_model (name, description, version, license, upload_date, update_date, download_count, view_count, user_id, username, torrent_file, magnet_link, model_img, file_size, tag)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, description, version, license, upload_date, update_date, download_count, view_count,
                    user_id, username, torrent_file_path, magnet_link, model_img,
                    file_size, ','.join(tags)
                ))
                connection.commit()
                print("模型数据插入成功")
        except Exception as e:
            connection.rollback()
            print(f"模型数据插入失败: {e}")
        finally:
            connection.close()
        return redirect(url_for('user.success_page'))


@user.route('/success')
def success_page():
    login_form = LoginForm()
    register_form = RegistrationForm()
    return render_template('success_page.html', login_form=login_form, register_form=register_form)
