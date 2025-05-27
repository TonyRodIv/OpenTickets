from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.gerenciar_sala import listar_salas, adicionar_sala, editar_sala, carregar_salas, deletar_sala
from data.gerenciar_filmes import carregar_json, salvar_json, ARQUIVO_FILMES, ARQUIVO_SALAS

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')

@adm_route.route('/')
def admInit():
    # Salas - adm
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    editarSala = url_for('adm.editar_sala_view')
    deletarSala = url_for('adm.deletar_sala_view')

    # Filmes - Adm
    listarFilmes = url_for('listar_filmes_view')
    adicionarFilme = url_for('adicionar_filme_view')
    editarFilme = url_for('editar_filme_view')
    deletarFilme = url_for('remover_filme_view')
    return render_template('admHome.html', listarSala=listarSala, adicionarSala=adicionarSala,
                           editarSala=editarSala, deletarSala=deletarSala,
                           listarFilmes=listarFilmes, adicionarFilme=adicionarFilme,
                           editarFilme=editarFilme, deletarFilme=deletarFilme)

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
def carregar_filmes():
    return carregar_json(ARQUIVO_FILMES)

def carregar_salas():
    return carregar_json(ARQUIVO_SALAS)

@adm_route.route('/listar_filmes')
def listar_filmes_view():
    filmes = carregar_filmes()
    return render_template('listar_filmes.html', filmes=filmes)

@adm_route.route('/adicionar_filme', methods=['GET', 'POST'])
def adicionar_filme_view():
    salas = carregar_salas()
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        duracao = int(request.form['duracao'])
        classificacao = request.form['classificacao'].strip()
        genero = request.form['genero'].strip()
        salas_escolhidas = request.form.getlist('salas')
        filmes = carregar_filmes()
        if any(f['titulo'].lower() == titulo.lower() for f in filmes):
            flash(f"Filme '{titulo}' já existe.", 'danger')
            return redirect(url_for('adm.adicionar_filme_view'))
        for s_id in salas_escolhidas:
            if any(s_id in f.get('salas', []) for f in filmes):
                flash(f"Sala {s_id} já está ocupada por outro filme.", 'danger')
                return redirect(url_for('adm.adicionar_filme_view'))
        filmes.append({
            "titulo": titulo,
            "duracao": duracao,
            "classificacao": classificacao,
            "genero": genero,
            "salas": salas_escolhidas
        })
        salvar_json(filmes, ARQUIVO_FILMES)
        flash(f"Filme '{titulo}' adicionado.", 'success')
        return redirect(url_for('adm.listar_filmes_view'))
    return render_template('adicionar_filme.html', salas=salas)

@adm_route.route('/editar_filme/<titulo>', methods=['GET', 'POST'])
def editar_filme_view(titulo):
    filmes = carregar_filmes()
    salas = carregar_salas()
    filme = next((f for f in filmes if f['titulo'].lower() == titulo.lower()), None)
    if not filme:
        flash(f"Filme '{titulo}' não encontrado.", 'danger')
        return redirect(url_for('adm.listar_filmes_view'))
    if request.method == 'POST':
        novo_titulo = request.form['titulo'].strip()
        duracao = int(request.form['duracao'])
        classificacao = request.form['classificacao'].strip()
        genero = request.form['genero'].strip()
        salas_escolhidas = request.form.getlist('salas')
        if novo_titulo.lower() != filme['titulo'].lower() and any(f['titulo'].lower() == novo_titulo.lower() for f in filmes):
            flash(f"Já existe filme com título '{novo_titulo}'.", 'danger')
            return redirect(url_for('adm.editar_filme_view', titulo=titulo))
        for s_id in salas_escolhidas:
            if s_id not in filme['salas'] and any(s_id in f.get('salas', []) for f in filmes):
                flash(f"Sala {s_id} já está ocupada por outro filme.", 'danger')
                return redirect(url_for('adm.editar_filme_view', titulo=titulo))
        filme['titulo'] = novo_titulo
        filme['duracao'] = duracao
        filme['classificacao'] = classificacao
        filme['genero'] = genero
        filme['salas'] = salas_escolhidas
        salvar_json(filmes, ARQUIVO_FILMES)
        flash(f"Filme '{novo_titulo}' atualizado.", 'success')
        return redirect(url_for('adm.listar_filmes_view'))
    return render_template('editar_filme.html', filme=filme, salas=salas)

@adm_route.route('/remover_filme/<titulo>', methods=['GET', 'POST'])
def remover_filme_view(titulo):
    filmes = carregar_filmes()
    filme = next((f for f in filmes if f['titulo'].lower() == titulo.lower()), None)
    if not filme:
        flash("Filme não encontrado.", 'danger')
        return redirect(url_for('adm.listar_filmes_view'))
    if request.method == 'POST':
        # Lógica de remoção aqui
        return redirect(url_for('adm.listar_filmes_view'))
    return render_template('remover_filme.html', filme=filme)


# GERENCIAR ASSENTOS


