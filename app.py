from crypt import methods
from distutils.debug import DEBUG
from email.mime import application
from unicodedata import name
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_wtf.csrf import CSRFProtect 
from forms import SignupForm, LoginForm, RegisterForm
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request
import requests
from pickle import GET
from unittest import result
from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user

 
client = MongoClient('localhost', 27017)
db = client.user
order_db = client.order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'


# flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_veiw = 'signUp'


@login_manager.user_loader
def load_user(username) :
  return db.users.find_one({'username' : username})

  
  
@app.route('/', methods=['GET'])
def home():
    now = datetime.now()
    current_day = now.strftime("%y%m%d")
    current_time = int(now.strftime("%H%M"))
    today_posts_list = list(order_db.posts.find({'date': {"$in" : [current_day]}}).sort('deadline', 1))
    posts_list = []
    for post in today_posts_list :
      hour,min = post['deadline'].split(':')
      deadline_time = int(hour+min)
 
      if current_time - deadline_time <= 0 :
                posts_list.append(post)

    if "username" in session : 
        return render_template('index.html', username = session.get("username"), login=True, orders=posts_list, token = session.get("csrf_token"))
    else : 
        return render_template('index.html', login=False, orders=posts_list)


@app.route('/register', methods=['GET','POST'])
def register():
    now = datetime.now()
    form = RegisterForm()
    if request.method == 'GET' :
      return render_template('register.html', username = session.get("username"), form = form, login=True)
    else :
      session.get("username")
      if form.validate_on_submit():
        register_user = session.get("username")  
        register_date = now.strftime("%y%m%d")
        shop_receive = form.shop.data
        min_num_receive = form.min_person.data
        deadline_receive = form.deadline.data
        delivery_cost_receive = form.delivery_cost.data
        open_url_receive = form.open_url.data

        post = {'register_user' : register_user, 'date': register_date,'shop': shop_receive, 'min_num': min_num_receive, 'deadline': deadline_receive,
                'delivery_cost': delivery_cost_receive, 'open_url': open_url_receive, 'user_list': []}  # user 변수 list에 저장
        
        order_db.posts.insert_one(post)

      
      else :
        flash("정확한 값을 입력해주세요!")
        return render_template("register.html", form = form)
      
    return redirect(url_for("home"))

@app.route('/spec/<objectId>', methods=['GET'])
def spec(objectId):

    post = order_db.posts.find_one({'_id':ObjectId(objectId)})
    if "username" in session :
        return render_template('detail.html', username = session.get("username"), login=True, post=post, objectId= objectId)
    else : 
        return render_template('detail.html', login=False, post=post)

@app.route('/together', methods=['POST'])
def together():
    id_receive = request.form['objectId']
    user_receive = request.form['user_id']  
    post = order_db.posts.find_one({'_id': ObjectId(id_receive)})
    open_url = post['open_url']
    post['user_list'].append(user_receive)
    order_db.posts.update_one({'_id': ObjectId(id_receive)}, {
                        '$set': {'user_list': post['user_list']}})

    return jsonify({'result': 'success', 'open_url': post['open_url']})

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
        session['username'] = user['username']
        return redirect(url_for("home", login=True))
      else : 
        flash("아이디, 비밀번호가 정확하지 않습니다!")
        return render_template("signIn.html", form = form)
    else :
        flash("아이디, 비밀번호가 정확하지 않습니다!")
        return render_template("signIn.html", form = form)
    
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
          flash("아이디가 이미 사용되었습니다.")
          return render_template("signUp.html", form = form)
        else : 
          hashed_pw = generate_password_hash(password)
          db.users.insert_one({'username':username, 'password':hashed_pw})
          user = db.users.find_one({'username' : username},{'_id':False})
          if user and check_password_hash(user['password'], form.password.data) :
            session['user'] = user
          return redirect(url_for("login"))

    else :
      flash("입력값을 다시 확인해주세요!")
      return redirect('/signup', form=form)
      
@app.route('/logout')
def logout():
  session.pop("username")
  return redirect(url_for("home"))
  
  

if __name__ == '__main__':
  WTF_CSRF_SECRET_KEY="a csrf secret key"
  csrf = CSRFProtect()
  csrf.init_app(app)
  app.run('0.0.0.0', port=5000, debug=True)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
