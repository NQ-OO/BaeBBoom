from crypt import methods
from distutils.debug import DEBUG
from email.mime import application
import imp
from unicodedata import name
from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect 
from forms import SignupForm, LoginForm, RegisterForm
# from wtforms import StringField, submitField
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request
import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


from pickle import GET
from unittest import result
from datetime import datetime
#from wtforms import StringField, submitField
# from wtforms.validators import DataRequired
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user

 
client = MongoClient('localhost', 27017)
db = client.user
order_db = client.order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'
app.config["JWT_SECRET_KEY"] = "dfafdjfdkfajfa;jieng"  
jwt = JWTManager(app)


# flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_veiw = 'signUp'


@login_manager.user_loader
def load_user(username) :
  return db.users.find_one({'username' : username})

  
  
@app.route('/', methods=['GET'])
def home():
    # 등록페이지
    now = datetime.now()
    current = int(now.strftime("%y%m%d%H%M"))
    # posts_list = list(db.posts.find({'deadline': {"$gte" : current}}).sort('deadline', 1))
    posts_list = list(order_db.posts.find({}))
    
    if "username" in session : 
        print(session)
        return render_template('index.html', username = session.get("username"), login=True, orders=posts_list)
    else : 
        return render_template('index.html', login=False, orders=posts_list)
      
    # posts_list = list(db.posts.find({'deadline': {"$gte" : current}}).sort('deadline', 1))

    # if "user" in session : 
    #     print(session)
    #     return render_template('index.html', username = session.get("user")["username"], login=True, orders=posts_list)
    # else : 
    #     return render_template('index.html', login=False, orders=posts_list)



# 리스트 출력하기
# <<<<<<< youngji
# @app.route('/list',methods=['GET'])
# def posts_list():
     
#     all_posts_list = list(db.posts.find({}).sort('deadline', 1))
#     posts_list = []
#     for posts in all_posts_list : 
#         register_date = datetime.strptime(posts['date'],"%Y%m%d")
#         #0. if문 해서 시간내에 있는거만 검색하기
#         if (now - register_date).days == 0 :
#             print("날짜 오늘")
#             if current_time - posts['deadline'] >= 0 :
#                 print("시간도 아직 안지남")
#                 posts_list.append(posts)

#     #2. 성공하면 success메시지와 목록을 클라이언트로 보내주기
#     return jsonify({'result':'success', 'posts' : posts_list})



# @app.route('/list', methods=['GET'])
# def posts_list():
#     # 0. if문 해서 시간내에 있는거만 검색하기

#     # 해당 post를 id를 제외하고 정렬
#     posts_list = list(db.posts.find({}, {'_id': False}).sort('deadline', 1))

#     # 2. 성공하면 success메시지와 목록을 클라이언트로 보내주기
#     return jsonify({'result': 'success', 'posts': posts_list})



# 등록페이지


@app.route('/register', methods=['GET','POST'])
def register():
    
    now = datetime.now()
    form = RegisterForm()
    if request.method == 'GET' :
      return render_template('register.html', username = session.get("username"), form = form, login=True)
    else :
      # # 1. 클라이언트 데이터 받기
      ####username, jwt,
      session.get("username")
      if form.validate_on_submit():
        register_user = session.get("username")  
        print("debug")
        register_date = now.strftime("%y%m%d")
        ######################### deadline_receive = int(now.strftime("%y%m%d") + request.form['realtime'])#######TODO###########
        shop_receive = form.shop.data
        min_num_receive = form.min_person.data
        deadline_receive = form.deadline.data
        delivery_cost_receive = form.delivery_cost.data
        open_url_receive = form.open_url.data


        post = {'register_user' : register_user, 'date': register_date,'shop': shop_receive, 'min_num': min_num_receive, 'deadline': deadline_receive,
                'delivery_cost': delivery_cost_receive, 'open_url': open_url_receive, 'user_list': []}  # user 변수 list에 저장
        
        # 2. mongoDB에 데이터 넣기
        order_db.posts.insert_one(post)

      
      else :
        flash("정확한 값을 입력해주세요!")
        print(form.data)
        return render_template("register.html", form = form)
      
    return redirect(url_for("home"))
 
    

# 상세페이지

@app.route('/spec/<objectId>', methods=['GET'])
def spec(objectId):
  # 1. 클라이언트에서 전달 받은 objectid 값을 변수에 넣는다.

    # 2. 해당 정보 찾기
    post = order_db.posts.find_one({'_id':ObjectId(objectId)})
    
    
    if "username" in session :
        print(session)
        return render_template('detail.html', username = session.get("username"), login=True, post=post)
    else : 
        return render_template('detail.html', login=False, post=post)


# 함께하기

@app.route('/together', methods=['POST'])
# @jwt_required
def together():
    # 1. 클라이언트에서 전달 받은 objectid 값을 변수에 넣는다.
    
    id_receive = request.form['objectId']
    user_receive = request.form['user_id']  # 유저 변수에 저장
    print("debug")


    # 2. 해당 정보 찾기
    post = order_db.posts.find_one({'_id': ObjectId(id_receive)})
    open_url = post['open_url']
    print("open_url :", open_url)

    # 3. user_list에 현재 사용자 추가
    #new_num = post['num']+1
    post['user_list'].append(user_receive)

    # 4. 해당 변수 저장해주기
    db.posts.update_one({'_id': ObjectId(id_receive)}, {
                        '$set': {'user_list': post['user_list']}})

    # 5. 링크 보내기
    return jsonify({'result': 'success', 'open_url': post['open_url']})

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
        access_token = create_access_token(identity={"username" : username})
        print(access_token)
        session['username'] = user['username']
        print(session)
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
  session.pop("username")
  return render_template('index.html', login=False)
  
  

if __name__ == '__main__':
  # WTF_CSRF_SECRET_KEY="a csrf secret key"
  # csrf = CSRFProtect()
  # csrf.init_app(app)
  app.run('0.0.0.0', port=5000, debug=True)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
