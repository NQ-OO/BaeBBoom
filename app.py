from crypt import methods
from distutils.debug import DEBUG
from email.mime import application
import imp
from unicodedata import name
from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect 
from forms import SignupForm, LoginForm
# from wtforms import StringField, submitField
# from wtforms.validators import DataRequired
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user

 
client = MongoClient('localhost', 27017)
db = client.user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

# flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_veiw = 'signUp'


@login_manager.user_loader
def load_user(username) :
  return db.users.find_one({'username' : username})

#@login_required


# application.config.update(
#   DEBUG = True, 

# )


# 메인페이지
@app.route('/')
def home():
  if "user" in session : 
    print(session)
    return render_template('index.html', username = session.get("user")["username"], login=True)
  else : 
    return render_template('index.html', login=False)

# 등록페이지
@app.route('/register')
def register():
    return render_template('register.html')

# 상세페이지


@app.route('/spec')
def spec():
    return render_template('detail.html')

# 로그인 페이지


@app.route('/signin', methods = ['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == "GET" :
    return render_template('signIn.html', form = form)
  else :
    if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = db.users.find_one({'username' : username},{'_id':False})
      if user and check_password_hash(user['password'], form.password.data) :
        session['user'] = user
        return redirect(url_for("home"))
      else : 
        flash("아이디, 비밀번호가 정확하지 않습니다!")
        return render_template("signIn.html", form = form)
        
      
      # if 
    return render_template('signIn.html', form = form)
    

# 회원가입 페이지
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
  form = SignupForm()
  if request.method == "GET":
    return render_template("signUp.html", form = form)
  else :    
    if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      password_check = form.password_check.data
      
      if password != password_check :
        flash("비밀번호를 확인해주세요!")
        return render_template("signUp.html", form = form)
      
      else :
        user_unique_check = db.users.find_one({'username' : username})
        if user_unique_check :
          print('debug')
          flash("아이디가 이미 사용되었습니다.")
          return render_template("signUp.html", form = form)
        else : 
          hashed_pw = generate_password_hash(password)
          db.users.insert_one({'username':username, 'password':hashed_pw})
          user = db.users.find_one({'username' : username},{'_id':False})
          if user and check_password_hash(user['password'], form.password.data) :
            session['user'] = user
          return redirect(url_for("home"))

    else :
      flash("입력값을 다시 확인해주세요!")
      return redirect('/signup', form=form)
      
@app.route('/logout')
def logout():
  session.pop("user")
  return render_template('index.html', login=False)
  
  
      
    
  


if __name__ == '__main__':
  WTF_CSRF_SECRET_KEY="a csrf secret key"

  csrf = CSRFProtect()
  csrf.init_app(app)
  
  
  app.run('0.0.0.0', port=5000, debug=True)


#Invalid URL
@app.errorhandler(404) 
def page_not_found(e):
  return render_template("404.html"), 404



    
  