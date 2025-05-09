from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
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