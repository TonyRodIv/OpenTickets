from flask import Blueprint, render_template, request, redirect, url_for, flash, session

login_route = Blueprint('login', __name__, template_folder='../templates')

@login_route.route('/', methods=['GET', 'POST']) 
def loginUser(): 

    return render_template('index.html') 