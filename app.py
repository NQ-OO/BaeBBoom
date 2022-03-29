


from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request
import requests
# from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
# from forms import SignupForm
# from asyncio.windows_events import NULL

from pickle import GET
from unittest import result
from datetime import datetime
#from wtforms import StringField, submitField
# from wtforms.validators import DataRequired


app = Flask(__name__)
print(app.config)

client = MongoClient('localhost', 27017)
db = client.dbjungle

now = datetime.now()
current_time = int(now.strftime("%H%M"))

# 메인페이지


# @app.route('/')
# def home():
#     return render_template('index.html')
@app.route('/', methods=['GET'])
def home():
    all_posts_list = list(db.posts.find({}).sort('deadline', 1))
    posts_list = []
    for posts in all_posts_list :
        register_date = datetime.strptime(posts['date'],"%y%m%d")
        print(type(posts['deadline']))
        # print(posts['deadline'])
        print(type(current_time))
        # print(current_time)
        # 0. if문 해서 시간내에 있는거만 검색하기
        # deadline = int(posts['deadline'])
        if (now - register_date).days == 0 :
            # print("날짜 오늘")
            if posts['deadline'] - current_time >= 0 :
                # print("시간도 아직 안지남")
                posts_list.append(posts)

    return render_template('index.html', orders=posts_list)

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

@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():

    # # 1. 클라이언트 데이터 받기
    register_date = now.strftime("%y%m%d")
    shop_receive = request.form['business_name']
    min_num_receive = request.form['min_per']

    deadline_receive = int(request.form['realtime'])

    delivery_cost_receive = request.form['fee']
    open_url_receive = request.form['open_link']
    user_receive = request.form['user_id']  # 유저 변수에 저장


    post = {'date': register_date,'shop': shop_receive, 'min_num': min_num_receive, 'deadline': deadline_receive,
            'delivery_cost': delivery_cost_receive, 'open_url': open_url_receive, 'user_list': [user_receive]}  # user 변수 list에 저장


    # 2. mongoDB에 데이터 넣기
    db.posts.insert_one(post)
    

    return jsonify({'result': 'success'})


# 상세페이지

@app.route('/spec/<objectId>', methods=['GET'])
def spec(objectId):
    # 1. 클라이언트에서 전달 받은 objectid 값을 변수에 넣는다.
    id_receive =  objectId

    # 2. 해당 정보 찾기
    post = db.posts.find_one({'_id':ObjectId(objectId)})
    
    # 3. 해당 정보 보냐쥬기 - id 제외하고????
    return render_template('detail.html', post=post)


# 함께하기

@app.route('/together', methods=['POST'])
def together():
    # 1. 클라이언트에서 전달 받은 objectid 값을 변수에 넣는다.
    id_receive = request.form['object_id_give']
    user_receive = request.form['user_give']  # 유저 변수에 저장

    # 2. 해당 정보 찾기
    post = db.posts.find_one({'_id': id_receive})
    open_url = post['open_url']

    # 3. user_list에 현재 사용자 추가
    #new_num = post['num']+1
    new_user_list = post['user_list'].append(user_receive)

    # 4. 해당 변수 저장해주기
    db.posts.update_one({'_id': id_receive}, {
                        '$set': {'user_list': new_user_list}})

    # 5. 링크 보내기
    return jsonify({'result': 'success', 'open_url': open_url})

# 로그인 페이지


@app.route('/signin')
def login():
    return render_template('signIn.html')

# 회원가입 페이지


@app.route('/signup')
def signup():

    return render_template('signUp.html')


if __name__ == '__main__':
    # app.config['SECRET_KEY'] = "secret_key"
    # csrf = CSRFProtect()
    # csrf.init_app(app)


    app.run('0.0.0.0', port=5000, debug=True)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
