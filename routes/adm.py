from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.gerenciar_sala import listar_salas, adicionar_sala, editar_sala, carregar_salas, deletar_sala
from data.gerenciar_filmes import adicionar_filme_web, carregar_filmes, listar_filmes

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')

@adm_route.route('/')
def admInit():
    # Salas - adm
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    editarSala = url_for('adm.editar_sala_view')
    deletarSala = url_for('adm.deletar_sala_view')

    # Filmes - Adm
    adicionarFilme = url_for('adm.adicionar_filme_view')
    return render_template('admHome.html', listarSala=listarSala, adicionarSala=adicionarSala,
                           editarSala=editarSala, deletarSala=deletarSala, adicionarFilme=adicionarFilme)

# GERENCIAR SALAS

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

# GERENCIAR FILMES
@adm_route.route('/adicionar_filme', methods=['GET', 'POST'])
def adicionar_filme_view():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        duracao = request.form.get('duracao', '').strip()
        classificacao = request.form.get('classificacao', '').strip()
        genero = request.form.get('genero', '').strip()
        urlFoto = request.form.get('urlFoto', '').strip()
        salas_escolhidas = request.form.getlist('salas') # Usa getlist para múltiplos checkboxes

        sucesso, mensagem = adicionar_filme_web(
            titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas
        )

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('adm.admInit')) # Redireciona para o início por enquanto
        else:
            flash(mensagem, 'danger')
            # Se der erro, renderiza o formulário novamente com as salas
            salas_disponiveis = carregar_salas()
            return render_template('adicionar_filme.html', salas=salas_disponiveis)

    # GET: Carrega as salas e exibe o formulário
    salas_disponiveis = carregar_salas()
    return render_template('adicionar_filme.html', salas=salas_disponiveis)


# GERENCIAR ASSENTOS


