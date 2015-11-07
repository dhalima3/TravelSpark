from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "YHacks woooo"

if __name__ == '__main__':
    app.run()

@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
