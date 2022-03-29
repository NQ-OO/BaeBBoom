from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignupForm (FlaskForm):
  username = StringField('username', validator=[DataRequired()])
  password = PasswordField('password', validator=[DataRequired(), EqualTo('password_check')])
  password_check = PasswordField('password_check', validator=[DataRequired()])
  submit = SubmitField("Submit")
  
  
