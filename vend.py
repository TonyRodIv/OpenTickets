from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from data.gerenciar_sala import carregar_salas
from data.gerenciar_filmes import filmes as lista_filmes
from data.gerenciar_assentos import carregar_assentos, salvar_assentos, init_sala, gerar_mapa

vend_route = Blueprint('vend', __name__, url_prefix='/vend', template_folder='../templates/vend')

@vend_route.route('/')
def vendInit():
    escolher_filme = url_for('vend.escolher_filme_view')
    escolher_sala = url_for('vend.escolher_sala_view')
    mapa_assentos = url_for('vend.mapa_assentos_view')
    confirmar_venda = url_for('vend.confirmar_venda_view')
    return render_template('vendHome.html', escolher_filme=escolher_filme, escolher_sala=escolher_sala,
                           mapa_assentos=mapa_assentos, confirmar_venda=confirmar_venda)

@vend_route.route('/escolher_filme', methods=['GET', 'POST'])
def escolher_filme():
    if request.method == 'POST':
        filme_idx = int(request.form.get('filme')) - 1
        session['filme'] = lista_filmes[filme_idx]
        return redirect(url_for('vend.escolher_sala'))
    
    return render_template('escolher_filme.html', filmes=lista_filmes)

@vend_route.route('/escolher_sala', methods=['GET', 'POST'])
def escolher_sala():
    filme = session.get('filme')
    salas = carregar_salas()
    salas_filme = [s for s in salas if s['numero'] in filme.get('salas', [])]

    if request.method == 'POST':
        sala_num = int(request.form.get('sala'))
        session['sala_num'] = sala_num
        return redirect(url_for('vend.mapa_assentos'))
    
    return render_template('escolher_sala.html', salas=salas_filme)

@vend_route.route('/mapa_assentos', methods=['GET', 'POST'])
def mapa_assentos():
    sala_num = session.get('sala_num')
    assentos = carregar_assentos()
    sala = next(s for s in carregar_salas() if s['numero'] == sala_num)
    
    init_sala(assentos, sala_num, sala['linhas'], sala['colunas'])
    mapa = gerar_mapa(assentos[sala_num])

    if request.method == 'POST':
        assento = request.form.get('assento').upper()
        if assentos[sala_num].get(assento, False):
            flash('Assento já ocupado!', 'danger')
            return redirect(url_for('vend.mapa_assentos'))
        
        assentos[sala_num][assento] = True
        salvar_assentos(assentos)
        session['assento'] = assento
        return redirect(url_for('vend.confirmar_venda'))

    return render_template('mapa_assentos.html', mapa=mapa)

@vend_route.route('/confirmar_venda')
def confirmar_venda():
    return render_template('confirmar_venda.html',
                           filme=session.get('filme'),
                           sala_num=session.get('sala_num'),
                           assento=session.get('assento'))
