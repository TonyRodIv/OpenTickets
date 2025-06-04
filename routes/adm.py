from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from data.gerenciar_sala import adicionar_sala, editar_sala, carregar_salas, deletar_sala
from data.gerenciar_filmes import adicionar_filme_web, carregar_filmes, salvar_json, editar_filme, ARQUIVO_FILMES
from data.gerenciar_vendas import calcular_vendas, filmes_populares

adm_route = Blueprint('adm', __name__, url_prefix='/adm', template_folder='../templates/adm')


CLASSIFICACOES_INDICATIVAS = ["Livre", "10 anos", "12 anos", "14 anos", "16 anos", "18 anos"]

GENEROS_FILME = ["Ação", "Animação", "Aventura", "Comédia", "Documentário", "Drama",
                 "Fantasia", "Ficção Científica", "Guerra", "Musical", "Policial", "Romance",
                 "Show", "Suspense", "Terror", "Thriller"]


@adm_route.route('/', methods=['GET', 'POST'])
def login(): # Função de login do ADM, está em /adm/
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'adm' and password == 'adm':
            return redirect(url_for('adm.admInit'))

        else:
            return redirect(url_for('adm.login'))

    return render_template('login.html')

@adm_route.route('/home')
def admInit():
    listarSala = url_for('adm.listar_salas_view')
    adicionarSala = url_for('adm.adicionar_sala_view')
    editarSala = url_for('adm.editar_sala_view')

    adicionarFilme = url_for('adm.adicionar_filme_view')
    listarFilmes = url_for('adm.listar_filmes_view')
    editarFilme = url_for('adm.editar_filme_view')
    relatorioVendas = url_for('adm.relatorio_vendas_view')

    top_filmes = filmes_populares(top_n=5)

    return render_template('admHome.html',
                           listarSala=listarSala,
                           adicionarSala=adicionarSala,
                           editarSala=editarSala,
                           adicionarFilme=adicionarFilme,
                           listarFilmes=listarFilmes,
                           editarFilme=editarFilme,
                           relatorioVendas=relatorioVendas,
                           filmes_populares=top_filmes)
    

@adm_route.route('/api/dados', methods=['GET'])
def api_listar_dados():
    filmes = carregar_filmes()
    salas = carregar_salas()
    return jsonify({'filmes': filmes, 'salas': salas})

# GERENCIAR SALAS -----------

@adm_route.route('/listar_salas')
def listar_salas_view():
    salas_cadastradas = carregar_salas() #
    filmes_cadastrados = carregar_filmes() #
    
    salas_para_template = []

    for sala_data in salas_cadastradas:
        sala_com_info = {
            'numero': sala_data['numero'],
            'capacidade': int(sala_data['linhas']) * int(sala_data['colunas']),
            'horarios_disponiveis': sala_data.get('horarios', []),
            'filmes_em_exibicao': [] 
        }
        
        for filme_data in filmes_cadastrados:
            if str(sala_data['numero']) in filme_data.get('salas', []):
                sala_com_info['filmes_em_exibicao'].append({
                    'titulo': filme_data['titulo'],
                    'urlFoto': filme_data.get('urlFoto', '')
                })
        
        salas_para_template.append(sala_com_info)
        
    return render_template('listar_salas.html', salas=salas_para_template)

@adm_route.route('/adicionar_sala', methods=['GET', 'POST'])
def adicionar_sala_view():
    if request.method == 'POST':
        try:
            linhas = int(request.form.get('linhas', 0))
            colunas = int(request.form.get('colunas', 0))
            nova = adicionar_sala(linhas, colunas)
            return redirect(url_for('adm.listar_salas_view'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('adicionar_sala.html')

@adm_route.route('/editar_sala', methods=['GET', 'POST'])
def editar_sala_view():
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        try:
            linhas = int(request.form.get('linhas', 0))
            colunas = int(request.form.get('colunas', 0))
        except ValueError:
            return redirect(url_for('adm.editar_sala_view'))

        sala, erro = editar_sala(numero, linhas, colunas)
        if erro:
            return redirect(url_for('adm.editar_sala_view'))
        return redirect(url_for('adm.listar_salas_view'))
    salas = carregar_salas()
    return render_template('editar_sala.html', salas=salas)

@adm_route.route('/deletar_sala', methods=['POST'])
def deletar_sala_view():
    numero_sala_para_deletar = request.form.get('numero', '').strip()

    deletar_sala(numero_sala_para_deletar) 
    
    filmes = carregar_filmes() 
    filmes_foram_modificados = False

    for filme_atual in filmes:
        salas_deste_filme = filme_atual.get('salas', []) #
        if numero_sala_para_deletar in salas_deste_filme:
            salas_deste_filme.remove(numero_sala_para_deletar)
            filmes_foram_modificados = True
    
    if filmes_foram_modificados:
        salvar_json(filmes, ARQUIVO_FILMES) #
            
    return redirect(url_for('adm.listar_salas_view'))

# GERENCIAR FILMES -------------------

@adm_route.route('/adicionar_filme', methods=['GET', 'POST'])
def adicionar_filme_view():
    todos_os_filmes = carregar_filmes()
    salas_ocupadas = set()
    for filme in todos_os_filmes:
        for sala_id in filme.get('salas', []): 
            salas_ocupadas.add(str(sala_id))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        duracao = request.form.get('duracao', '').strip()
        classificacao = request.form.get('classificacao', '').strip()
        genero = request.form.get('genero', '').strip()
        urlFoto = request.form.get('urlFoto', '').strip()
        salas_escolhidas = request.form.getlist('salas')

        sucesso, mensagem = adicionar_filme_web(
            titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas
        )

        if sucesso:
            return redirect(url_for('adm.admInit'))
        else:
            salas_disponiveis = carregar_salas()
            return render_template('adicionar_filme.html', 
                                   salas=salas_disponiveis,
                                   classificacoes_indicativas=CLASSIFICACOES_INDICATIVAS,
                                   generos_filme=GENEROS_FILME,
                                   salas_ocupadas=salas_ocupadas) 

    salas_disponiveis = carregar_salas()
    return render_template('adicionar_filme.html',
                           salas=salas_disponiveis,
                           classificacoes_indicativas=CLASSIFICACOES_INDICATIVAS,
                           generos_filme=GENEROS_FILME,
                           salas_ocupadas=salas_ocupadas)

@adm_route.route('/listar_filmes')
def listar_filmes_view():
    filmes = carregar_filmes()
    return render_template('listar_filmes.html', filmes=filmes)

@adm_route.route('/editar_filme', methods=['GET', 'POST'])
def editar_filme_view():
    filmes = carregar_filmes() 
    salas = carregar_salas()

    if request.method == 'POST':
        titulo_original = request.form.get('titulo_original')
        if not titulo_original:
            return render_template('editar_filme.html', filmes=filmes, salas=salas)

        dados_novos = {
            'titulo': request.form['titulo'],
            'duracao': request.form['duracao'],
            'classificacao': request.form['classificacao'],
            'genero': request.form['genero'],
            'salas': request.form.getlist('salas')
        }

        if not all(dados_novos.values()):
             return render_template('editar_filme.html', filmes=filmes, salas=salas)

        sucesso, resultado = editar_filme(titulo_original, dados_novos)

        if sucesso:
            return redirect(url_for('adm.listar_filmes_view'))
        else:
            return render_template('editar_filme.html', filmes=filmes, salas=salas)

    return render_template('editar_filme.html', filmes=filmes, salas=salas, classificacoes_indicativas=CLASSIFICACOES_INDICATIVAS,
                           generos_filme=GENEROS_FILME)

@adm_route.route('/remover_filme/<titulo>', methods=['POST'])
def remover_filme_view(titulo): 
    filmes = carregar_filmes()
    filmes_filtrados = [f for f in filmes if f['titulo'].lower() != titulo.lower()]

    if len(filmes_filtrados) < len(filmes):
        salvar_json(filmes_filtrados, ARQUIVO_FILMES)

    return redirect(url_for('adm.listar_filmes_view'))


# GERENCIADOR DE VENDAS --------------

@adm_route.route('/relatorio_vendas_diarias', methods=['GET', 'POST'])
def relatorio_vendas_view():
    data_para_buscar = request.form.get('data_relatorio') if request.method == 'POST' else None
    resumo = calcular_vendas(data_para_buscar)
    
    return render_template('relatorio_vendas.html', resumo=resumo)


@adm_route.route('/filmes_mais_populares')
def filmes_mais_populares_view():

    filmes_populares = filmes_populares(top_n=5)
    return render_template('filmes_mais_populares.html', filmes_populares=filmes_populares)