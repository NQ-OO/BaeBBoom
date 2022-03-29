from flask import Flask, render_template
app = Flask(__name__)


# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

# 등록페이지


@app.route('/register')
def register():
    return 'This is 등록페이지!'

# 상세페이지


@app.route('/spec')
def spec():
    return 'This is 상세페이지!'

# 로그인 페이지


@app.route('/login')
def login():
    return 'This is 로그인페이지!'

# 회원가입 페이지


@app.route('/signup')
def signup():
    return 'This is 회원가입페이지!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
