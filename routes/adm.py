from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.gerenciar_sala import listar_salas, adicionar_sala

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')

@adm_route.route('/')
def admInit():
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    return render_template('admHome.html', listarSala=listarSala, adicionarSala=adicionarSala)

@adm_route.route('/listar_salas')
def listar_salas_view():
    salas = listar_salas()
    return render_template('listar_salas.html', salas=salas)

@adm_route.route('/adicionar_sala', methods=['GET', 'POST'])
def adicionar_sala_view():
    if request.method == 'POST':
        try:
            linhas = int(request.form.get('linhas', 0))
            colunas = int(request.form.get('colunas', 0))
            nova = adicionar_sala(linhas, colunas)
            flash(f"Sala {nova['numero']} adicionada com sucesso!", 'success')
            return redirect(url_for('adm.listar_salas_view'))
        except ValueError as e:
            flash(str(e), 'danger')
            # segue ao render abaixo exibindo mensagem de erro
    # GET ou erro de validação
    return render_template('adicionar_sala.html')
