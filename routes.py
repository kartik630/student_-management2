from flask import Blueprint, render_template

main = Blueprint('main',__name__)

@main.route('/home',methods=['GET'])
def home():
    return render_template('home.html')