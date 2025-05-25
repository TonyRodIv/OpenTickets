from flask import Blueprint, render_template

login_route = Blueprint('login', __name__)

@login_route.route('/')
def login():
    return render_template('login.html', textoTeste = 'Texto de teste')