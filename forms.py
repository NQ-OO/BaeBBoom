from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField, DateTimeField, URLField
from wtforms.validators import DataRequired, EqualTo


class SignupForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  password_check = PasswordField('password_check', validators=[DataRequired()])
  submit = SubmitField("회원가입")
  

class LoginForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  submit = SubmitField("로그인")


class RegisterForm(FlaskForm) :
  shop = StringField('username', validators=[DataRequired()])
  min_person = IntegerField('min_person', validators=[DataRequired()])
  deadline = StringField('deadline', validators=[DataRequired()])
  delivery_cost = StringField('delivery_cost', validators=[DataRequired()])
  open_url = StringField('open_url', validators=[DataRequired()])
  submit = SubmitField("등록하기")
