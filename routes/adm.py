from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from data.gerenciar_sala import adicionar_sala, editar_sala, carregar_salas, deletar_sala
from data.gerenciar_filmes import adicionar_filme_web, carregar_filmes, salvar_json, editar_filme, ARQUIVO_FILMES

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')

CLASSIFICACOES_INDICATIVAS = ["Livre", "10 anos", "12 anos", "14 anos", "16 anos", "18 anos"]
GENEROS_FILME = [
    "Ação", "Animação", "Aventura", "Comédia", "Documentário", "Drama",
    "Fantasia", "Ficção Científica", "Guerra", "Musical", "Policial", "Romance",
    "Show", "Suspense", "Terror", "Thriller"
]

@adm_route.route('/')
def admInit():
    # Salas - adm
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    editarSala = url_for('adm.editar_sala_view')

    # Filmes - Adm
    adicionarFilme = url_for('adm.adicionar_filme_view')
    listarFilmes = url_for('adm.listar_filmes_view')
    editarFilme = url_for('adm.editar_filme_view')
    return render_template('admHome.html', listarSala=listarSala, adicionarSala=adicionarSala,
                           editarSala=editarSala, adicionarFilme=adicionarFilme, listarFilmes=listarFilmes, editarFilme=editarFilme)

@adm_route.route('/api/filmes', methods=['GET'])
def api_listar_filmes():
    filmes = carregar_filmes()
    return jsonify(filmes) # Retorna a lista como um JSON para o JS interpretar

# GERENCIAR SALAS - a partir daqui!

@adm_route.route('/listar_salas')
def listar_salas_view():
    salas_dados = carregar_salas() 
    return render_template('listar_salas.html', salas=salas_dados) 

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

@adm_route.route('/deletar_sala', methods=['POST'])
def deletar_sala_view():
    numero_str = request.form.get('numero', '').strip()

    if not numero_str:
        flash("Número da sala não fornecido.", 'danger')
        return redirect(url_for('adm.listar_salas_view'))
    try:
        erro = deletar_sala(numero_str) 
        if erro:
            flash(erro, 'danger')
        else:
            flash(f"Sala {numero_str} removida com sucesso!", 'success') 
    except Exception as e:
        flash(f"Ocorreu um erro inesperado: {e}", 'danger')
        
    return redirect(url_for('adm.listar_salas_view'))

# GERENCIAR FILMES
@adm_route.route('/adicionar_filme', methods=['GET', 'POST'])
def adicionar_filme_view():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        duracao = request.form.get('duracao', '').strip()
        classificacao = request.form.get('classificacao', '').strip()
        genero = request.form.get('genero', '').strip()
        urlFoto = request.form.get('urlFoto', '').strip()
        salas_escolhidas = request.form.getlist('salas') # Usa getlist para váaaarios checkbox

        sucesso, mensagem = adicionar_filme_web(
            titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas
        )

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('adm.admInit')) # Redireciona para o início por enquanto (lemnbrar mudar depois)
        else:
            flash(mensagem, 'danger')
            # Se der erro, renderiza o formulário novamente com as salas
            salas_disponiveis = carregar_salas()
            return render_template('adicionar_filme.html', salas=salas_disponiveis)

    # GET: Carrega as salas e exibe o formulário
    salas_disponiveis = carregar_salas()
    return render_template('adicionar_filme.html',
                           salas=salas_disponiveis,
                           classificacoes_indicativas=CLASSIFICACOES_INDICATIVAS,
                           generos_filme=GENEROS_FILME)

@adm_route.route('/listar_filmes')
def listar_filmes_view():
    filmes = carregar_filmes()
    # usa a função para peegar os dados do json e dps renderiza o template, passando a lista de filmes para ele
    return render_template('listar_filmes.html', filmes=filmes)

@adm_route.route('/editar_filme', methods=['GET', 'POST'])
def editar_filme_view():
    filmes = carregar_filmes()  # Carrega a lista de filmes
    salas = carregar_salas()

    if request.method == 'POST':
        # Pega o título original do <select> no html por meio do id ou name do input (é um desses dois)
        titulo_original = request.form.get('titulo_original')
        if not titulo_original:
            flash("Você precisa selecionar um filme para editar.", 'danger')
            return render_template('editar_filme.html', filmes=filmes, salas=salas)

        # Pega os novos dados dos inputs
        dados_novos = {
            'titulo': request.form['titulo'],
            'duracao': request.form['duracao'],
            'classificacao': request.form['classificacao'],
            'genero': request.form['genero'],
            'salas': request.form.getlist('salas')
        }

        # Validações básicas (pode adicionar mais se necessário)
        if not all(dados_novos.values()): # Verifica se algum campo está vazio (exceto salas)
             flash("Todos os campos de texto e número são obrigatórios.", 'danger')
             return render_template('editar_filme.html', filmes=filmes, salas=salas)

        # Chama a função de negócio
        sucesso, resultado = editar_filme(titulo_original, dados_novos)

        if sucesso:
            flash(f"Filme '{resultado['titulo']}' atualizado com sucesso.", 'success')
            return redirect(url_for('adm.listar_filmes_view'))
        else:
            flash(resultado, 'danger') # Mostra o erro vindo da função
            # Re-renderiza a página mostrando o erro
            return render_template('editar_filme.html', filmes=filmes, salas=salas)

    # GET: Apenas mostra o formulário com a lista de filmes e salas
    return render_template('editar_filme.html', filmes=filmes, salas=salas, classificacoes_indicativas=CLASSIFICACOES_INDICATIVAS,
                           generos_filme=GENEROS_FILME)

@adm_route.route('/remover_filme/<titulo>', methods=['POST'])
def remover_filme_view(titulo): #
    """Rota para remover um filme pelo título."""
    filmes = carregar_filmes()
    filmes_filtrados = [f for f in filmes if f['titulo'].lower() != titulo.lower()]

    if len(filmes_filtrados) < len(filmes):
        salvar_json(filmes_filtrados, ARQUIVO_FILMES) # <--- MUDE AQUI!
        flash(f"Filme '{titulo}' removido com sucesso!", 'success')
    else:
        flash(f"Filme '{titulo}' não encontrado.", 'danger')

    return redirect(url_for('adm.listar_filmes_view'))

# GERENCIAR ASSENTOS


