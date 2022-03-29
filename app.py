from flask import Flask, render_template
app = Flask(__name__)


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


@app.route('/login')
def login():
    return render_template('signIn.html')

# 회원가입 페이지


@app.route('/signup')
def signup():
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
