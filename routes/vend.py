from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from data.gerenciar_sala import carregar_salas
from data.gerenciar_filmes import carregar_filmes
from data.gerenciar_assentos import carregar_assentos, salvar_assentos, init_sala, gerar_mapa

vend_route = Blueprint('vend', __name__, url_prefix='/vend', template_folder='../templates/vend')

@vend_route.route('/')
def vendInit():
    return render_template('vendHome.html')

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
    salas_disponiveis_para_filme = []

    # Iterar sobre as salas para adicionar seus horários
    for s in salas_cadastradas:
        if str(s.get('numero')) in salas_do_filme_ids:
            # Adiciona os horários à sala antes de passá-la para o template
            s['horarios'] = sorted(s.get('horarios', [])) # Garante que os horários estejam ordenados
            salas_disponiveis_para_filme.append(s)

    if request.method == 'POST':
        sala_num = request.form.get('sala')
        horario_selecionado = request.form.get('horario_selecionado') # Pega o horário da sala selecionada
        
        if not sala_num:
            flash("Por favor, selecione uma sala. 🤷‍♀️", "danger")
            return redirect(url_for('vend.escolher_sala'))
        if not horario_selecionado:
            flash("Por favor, selecione um horário para a sala. ⏰", "danger")
            return redirect(url_for('vend.escolher_sala')) # Redireciona para a mesma página

        session['sala_selecionada_num'] = sala_num
        session['horario_selecionado'] = horario_selecionado # Salva o horário na sessão
        return redirect(url_for('vend.mapa_assentos'))
    
    return render_template('escolher_sala.html', salas=salas_disponiveis_para_filme)

@vend_route.route('/mapa_assentos', methods=['GET', 'POST'])
def mapa_assentos():
    sala_num = session.get('sala_selecionada_num')
    filme = session.get('filme_selecionado')
    horario = session.get('horario_selecionado')
    
    if not sala_num or not filme or not horario: 
        flash("Ops! Algo deu errado. Comece a venda novamente. 🚧", "danger")
        return redirect(url_for('vend.vendInit'))

    todas_salas = carregar_salas()
    sala_obj = next((s for s in todas_salas if str(s['numero']) == str(sala_num)), None)

    if not sala_obj:
        flash("Sala não encontrada. 🕵️‍♀️", "danger")
        return redirect(url_for('vend.escolher_sala'))

    assentos_globais = carregar_assentos()
    
    init_sala(assentos_globais, str(sala_num), str(horario), sala_obj['linhas'], sala_obj['colunas'])
    
    mapa_visual = gerar_mapa(assentos_globais.get(str(sala_num), {}).get(str(horario), {}))

    
    PRICES = {
        'inteira': 25.00,
        'meia': 12.50
    }

    if request.method == 'POST':
        assentos_selecionados_com_tipo = {}
        for key in request.form:
            if key.startswith('assentos_comprados['):
                assento_code = key[key.find('[')+1 : key.find(']')]
                assentos_selecionados_com_tipo[assento_code] = request.form[key]

        if not assentos_selecionados_com_tipo:
            flash('Por favor, selecione pelo menos um assento e o tipo de ingresso. 🧐', 'danger')
            return redirect(url_for('vend.mapa_assentos'))

        venda_realizada = []
        for assento_code, tipo_ingresso in assentos_selecionados_com_tipo.items():
            if assentos_globais.get(str(sala_num), {}).get(str(horario), {}).get(assento_code, False):
                flash(f'O assento {assento_code} para o horário {horario} já está ocupado! Não foi possível vendê-lo. 🙅‍♀️', 'danger')
                continue 
            
            assentos_globais[str(sala_num)][str(horario)][assento_code] = True
            venda_realizada.append({'assento': assento_code, 'tipo': tipo_ingresso})

        if not venda_realizada:
            flash("Nenhum assento pôde ser vendido. Verifique os assentos selecionados. 😭", "danger")
            return redirect(url_for('vend.mapa_assentos'))
            
        salvar_assentos(assentos_globais)

        session['venda_detalhes'] = {
            'filme': filme,
            'sala_num': sala_num,
            'horario': horario, 
            'assentos': venda_realizada 
        }
        flash(f'Venda realizada com sucesso para {len(venda_realizada)} assento(s)! ✅', 'success')
        return redirect(url_for('vend.confirmar_venda'))

    return render_template('mapa_assentos.html', mapa=mapa_visual, filme=filme, sala_num=sala_num, sala_obj=sala_obj, horario=horario, PRICES=PRICES)

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
                           horario=venda_detalhes['horario'],
                           assentos_vendidos=venda_detalhes['assentos'],
                           total_compra=total_compra)