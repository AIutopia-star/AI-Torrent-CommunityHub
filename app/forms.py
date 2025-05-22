from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User
import pymysql.cursors

class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired()])  # 只保留必填验证
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired()])  # 只保留必填验证
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
    agree_terms = BooleanField('I agree to the Terms of Service', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='fCfi;iKup5>N',
                                     database='ai_torrent',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id FROM user WHERE email=%s"
                cursor.execute(sql, (email.data,))
                if cursor.fetchone():
                    raise ValidationError('Email already registered. Please use a different email.')
        finally:
            connection.close()

    def validate_username(self, username):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='fCfi;iKup5>N',
                                     database='ai_torrent',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id FROM user WHERE username=%s"
                cursor.execute(sql, (username.data,))
                if cursor.fetchone():
                    raise ValidationError('Username already taken. Please choose a different one.')
        finally:
            connection.close()

class ModelUploadForm(FlaskForm):
    name = StringField('Model Name', validators=[DataRequired()], render_kw={"placeholder": "Model name"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows": 3, "placeholder": "Detailed description of your model"})
    version = StringField('Version', validators=[DataRequired()], render_kw={"placeholder": "1.0.0"})
    license = SelectField('License', choices=[('MIT', 'MIT'), ('GPL', 'GPL'), ('Apache', 'Apache')], validators=[DataRequired()])
    tags = StringField('Tags', validators=[Optional()], render_kw={"placeholder": "Add tags separated by commas"})
    torrent_file = FileField('Torrent File', validators=[DataRequired()])
    model_img = FileField('Model Image', validators=[Optional()])  # 添加图片上传字段
    is_private = BooleanField('Private')