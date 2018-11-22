from flask import Blueprint
from flask import render_template

posts = Blueprint('posts', __name__, template_folder='templates')

@nav.route('/')
def index():
	return render_template('nav/index.html')