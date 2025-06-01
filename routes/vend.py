from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from data.gerenciar_sala import carregar_salas
from data.gerenciar_filmes import carregar_filmes
from data.gerenciar_assentos import carregar_assentos, salvar_assentos, init_sala, gerar_mapa

vend_route = Blueprint('vend', __name__, url_prefix='/vend', template_folder='../templates/vend')

@vend_route.route('/')
def vendInit():
    # Limpa a sessão ao iniciar uma nova venda para evitar dados antigos
    session.pop('filme_selecionado', None)
    session.pop('sala_selecionada_num', None)
    session.pop('venda_detalhes', None)
    escolher_filme = url_for('vend.escolher_filme')
    return render_template('vendHome.html', escolher_filme=escolher_filme)

@vend_route.route('/escolher_filme', methods=['GET', 'POST'])
def escolher_filme():
    lista_filmes = carregar_filmes()
    if request.method == 'POST':
        filme_idx = int(request.form.get('filme')) - 1
        session['filme_selecionado'] = lista_filmes[filme_idx] 
        return redirect(url_for('vend.escolher_sala'))
    
    return render_template('escolher_filme.html', filmes=lista_filmes)

@vend_route.route('/escolher_sala', methods=['GET', 'POST'])
def escolher_sala():
    filme = session.get('filme_selecionado')
    if not filme:
        flash("Por favor, selecione um filme primeiro. 🎬", "danger")
        return redirect(url_for('vend.escolher_filme'))

    salas_cadastradas = carregar_salas()
    salas_do_filme_ids = [str(s) for s in filme.get('salas', [])]
    salas_disponiveis_para_filme = [s for s in salas_cadastradas if str(s.get('numero')) in salas_do_filme_ids]

    if request.method == 'POST':
        sala_num = request.form.get('sala')
        if not sala_num:
            flash("Por favor, selecione uma sala. 🤷‍♀️", "danger")
            return redirect(url_for('vend.escolher_sala'))

        session['sala_selecionada_num'] = sala_num
        return redirect(url_for('vend.mapa_assentos'))
    
    return render_template('escolher_sala.html', salas=salas_disponiveis_para_filme)

@vend_route.route('/mapa_assentos', methods=['GET', 'POST'])
def mapa_assentos():
    sala_num = session.get('sala_selecionada_num')
    filme = session.get('filme_selecionado')
    
    if not sala_num or not filme:
        flash("Ops! Algo deu errado. Comece a venda novamente. 🚧", "danger")
        return redirect(url_for('vend.vendInit'))

    todas_salas = carregar_salas()
    # Encontra o objeto da sala completo, não apenas o número
    sala_obj = next((s for s in todas_salas if str(s['numero']) == str(sala_num)), None)

    if not sala_obj:
        flash("Sala não encontrada. 🕵️‍♀️", "danger")
        return redirect(url_for('vend.escolher_sala'))

    assentos_globais = carregar_assentos()
    init_sala(assentos_globais, str(sala_num), sala_obj['linhas'], sala_obj['colunas'])
    mapa_visual = gerar_mapa(assentos_globais.get(str(sala_num), {}))

    if request.method == 'POST':
        # Pega os assentos e tipos de ingresso do formulário
        # request.form.getlist('assentos_comprados[]') funcionaria se os nomes fossem assim.
        # Como usamos 'assentos_comprados[A1]', precisamos iterar.
        assentos_selecionados_com_tipo = {}
        for key in request.form:
            if key.startswith('assentos_comprados['):
                assento_code = key[key.find('[')+1 : key.find(']')] # Extrai 'A1' de 'assentos_comprados[A1]'
                assentos_selecionados_com_tipo[assento_code] = request.form[key] # Pega o tipo de ingresso

        if not assentos_selecionados_com_tipo:
            flash('Por favor, selecione pelo menos um assento e o tipo de ingresso. 🧐', 'danger')
            return redirect(url_for('vend.mapa_assentos'))

        venda_realizada = []
        for assento_code, tipo_ingresso in assentos_selecionados_com_tipo.items():
            if assentos_globais.get(str(sala_num), {}).get(assento_code, False):
                flash(f'O assento {assento_code} já está ocupado! Não foi possível vendê-lo. 🙅‍♀️', 'danger')
                continue 
            
            assentos_globais[str(sala_num)][assento_code] = True
            venda_realizada.append({'assento': assento_code, 'tipo': tipo_ingresso})

        if not venda_realizada:
            flash("Nenhum assento pôde ser vendido. Verifique os assentos selecionados. 😭", "danger")
            return redirect(url_for('vend.mapa_assentos'))
            
        salvar_assentos(assentos_globais)

        session['venda_detalhes'] = {
            'filme': filme,
            'sala_num': sala_num,
            'assentos': venda_realizada 
        }
        flash(f'Venda realizada com sucesso para {len(venda_realizada)} assento(s)! ✅', 'success')
        return redirect(url_for('vend.confirmar_venda'))

    # Para requisições GET
    return render_template('mapa_assentos.html', mapa=mapa_visual, filme=filme, sala_num=sala_num, sala_obj=sala_obj)

@vend_route.route('/confirmar_venda')
def confirmar_venda():
    venda_detalhes = session.get('venda_detalhes')

    if not venda_detalhes:
        flash("Dados da venda incompletos. Por favor, reinicie a venda. 😭", "danger")
        return redirect(url_for('vend.vendInit'))
    
    PRICES = {
        'inteira': 25.00,
        'meia': 12.50
    }

    total_compra = 0
    for item in venda_detalhes['assentos']:
        total_compra += PRICES.get(item['tipo'], 0) 

    return render_template('confirmar_venda.html',
                           filme=venda_detalhes['filme'],
                           sala_num=venda_detalhes['sala_num'],
                           assentos_vendidos=venda_detalhes['assentos'],
                           total_compra=total_compra)