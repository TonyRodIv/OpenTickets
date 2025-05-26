from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.gerenciar_sala import listar_salas, adicionar_sala, editar_sala, carregar_salas, deletar_sala

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')

@adm_route.route('/')
def admInit():
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    editarSala = url_for('adm.editar_sala_view')
    deletarSala = url_for('adm.deletar_sala_view')
    return render_template('admHome.html', listarSala=listarSala, adicionarSala=adicionarSala,
                           editarSala=editarSala, deletarSala=deletarSala)

@adm_route.route('/listar_salas')
def listar_salas_view():
    salas = listar_salas()
    return render_template('listar_salas.html', salas=salas)

@adm_route.route('/adicionar_sala', methods=['GET', 'POST'])
def adicionar_sala_view():
    # POST: adiciona nova sala e volida os dados
    if request.method == 'POST':
        try:
            linhas = int(request.form.get('linhas', 0))
            colunas = int(request.form.get('colunas', 0))
            nova = adicionar_sala(linhas, colunas)
            flash(f"Sala {nova['numero']} adicionada com sucesso!", 'success')
            return redirect(url_for('adm.listar_salas_view'))
        except ValueError as e:
            flash(str(e), 'danger')
    # GET: apresenta formulário para adicionar sala
    return render_template('adicionar_sala.html')

@adm_route.route('/editar_sala', methods=['GET', 'POST'])
def editar_sala_view():
    # POST: edita sala e valida os dados
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        try:
            linhas = int(request.form.get('linhas', 0))
            colunas = int(request.form.get('colunas', 0))
        except ValueError:
            flash("Linhas e colunas devem ser números inteiros.", 'danger')
            return redirect(url_for('adm.editar_sala_view'))

        sala, erro = editar_sala(numero, linhas, colunas)
        if erro:
            flash(erro, 'danger')
            return redirect(url_for('adm.editar_sala_view'))

        flash(
            f"Sala {sala['numero']} atualizada: "
            f"{sala['linhas']} × {sala['colunas']} fileiras×colunas",
            'success'
        )
        return redirect(url_for('adm.listar_salas_view'))
    # GET: apresenta formulário com todas as salas
    salas = carregar_salas()
    return render_template('editar_sala.html', salas=salas)

@adm_route.route('/deletar_sala', methods=['GET', 'POST'])
def deletar_sala_view():
    # POST: deleta sala e valida os dados
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        erro = deletar_sala(numero)
        if erro:
            flash(erro, 'danger')
        else:
            flash(f"Sala {numero} removida com sucesso!", 'success')
        return redirect(url_for('adm.listar_salas_view'))
    # GET: apresenta formulário com todas as salas
    salas = carregar_salas()
    return render_template('deletar_sala.html', salas=salas)