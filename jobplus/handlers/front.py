from flask import Blueprint, render_template

front = Blueprint('front', __name__)

@front.route('/')
def index():
    return 'hello jobplus'
