from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@main.route('/home')
def home():
    return render_template('home.html')