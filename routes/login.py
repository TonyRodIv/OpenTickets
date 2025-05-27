from flask import Blueprint, render_template, request, redirect, url_for, flash, session

login_route = Blueprint('login', __name__, template_folder='../templates')

@login_route.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type') # Pega o tipo de usuário do select

        # Lógica de login atualizada
        if user_type == 'adm' and username == 'adm' and password == 'adm':
            session['user_type'] = 'adm'
            flash('Login de administrador bem-sucedido!', 'success')
            return redirect(url_for('adm.admInit'))

        elif user_type == 'vend' and username == 'vend' and password == 'vend':
            session['user_type'] = 'vend'
            flash('Login de vendedor bem-sucedido!', 'success')
            return redirect(url_for('vend.vendInit'))

        else:
            flash('Usuário, senha ou tipo de usuário inválidos.', 'danger')
            return redirect(url_for('login.login'))

    session.pop('user_type', None)
    return render_template('index.html')