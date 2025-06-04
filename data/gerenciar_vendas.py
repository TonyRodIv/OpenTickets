import json
import os
from datetime import datetime
from collections import Counter

ARQUIVO_VENDAS = os.path.join('data', 'temp', 'vendas.json')

def garantir_pasta_vendas():
    pasta = os.path.dirname(ARQUIVO_VENDAS)
    os.makedirs(pasta, exist_ok=True)

def carregar_vendas():
    garantir_pasta_vendas()
    if os.path.exists(ARQUIVO_VENDAS):
        with open(ARQUIVO_VENDAS, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] 
    return []

def salvar_vendas(vendas):
    garantir_pasta_vendas()
    with open(ARQUIVO_VENDAS, 'w', encoding='utf-8') as f:
        json.dump(vendas, f, ensure_ascii=False, indent=4)

def registrar_venda(filme_titulo, sala_num, assento, tipo_ingresso, data_hora_venda=None):
    vendas = carregar_vendas()
    if data_hora_venda is None:
        data_hora_venda = datetime.now().isoformat()
    
    nova_venda = {
        "filme": filme_titulo,
        "sala": sala_num,
        "assento": assento,
        "tipo": tipo_ingresso,
        "data_hora": data_hora_venda
    }
    vendas.append(nova_venda)
    salvar_vendas(vendas)

def obter_vendas(data_str=None):
    vendas = carregar_vendas()
    
    if data_str is None:
        hoje = datetime.now().strftime('%d/%m/%Y')
    else:
        hoje = data_str
    
    vendas_do_dia = [
        venda for venda in vendas 
        if venda['data_hora'].startswith(hoje) or venda['data_hora'].split('T')[0] == hoje
    ]
    return vendas_do_dia

def calcular_vendas(data_str=None):
    vendas_feitas = obter_vendas(data_str)
    
    total_assentos = len(vendas_feitas)
    
    PRICES = {
        'inteira': 25.00,
        'meia': 12.50
    }
    total_arrecadado = 0.0
    for venda in vendas_feitas:
        tipo = venda.get('tipo', 'inteira')
        total_arrecadado += PRICES.get(tipo, 0.0)
        
    return {
        'data': data_str if data_str else datetime.now().strftime('%d/%m/%Y'),
        'total_assentos': total_assentos,
        'total_arrecadado': total_arrecadado,
        'detalhes_vendas': vendas_feitas
    }

def filmes_populares(top_n=5):
    vendas = carregar_vendas()
    
    titulos_vendidos = [venda['filme'] for venda in vendas]
    contagem_filmes = Counter(titulos_vendidos)
    
    return contagem_filmes.most_common(top_n)
