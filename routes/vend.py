from flask import Blueprint, render_template

vend_route = Blueprint('vend', __name__)

@vend_route.route('/')
def vend():
    return render_template('vend.html', textoTeste = 'Texto de teste')