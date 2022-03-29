from flask import Flask, render_template
# from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms import SignupForm
# from wtforms import StringField, submitField
# from wtforms.validators import DataRequired


app = Flask(__name__)
print(app.config)


# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

# 등록페이지


@app.route('/register')
def register():
    return render_template('register.html')

# 상세페이지


@app.route('/spec')
def spec():
    return render_template('detail.html')

# 로그인 페이지


@app.route('/signin')
def login():
    return render_template('signIn.html')

# 회원가입 페이지


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = "secret_key"
    csrf = CSRFProtect()
    csrf.init_app(app)

    app.run('0.0.0.0', port=5000, debug=True)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
