import json, os

ARQUIVO = os.path.join('data','temp','assentos.json')

def garantir_pasta():
    pasta = os.path.dirname(ARQUIVO)
    os.makedirs(pasta, exist_ok=True)

def carregar_assentos():
    garantir_pasta()
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {} 

def salvar_assentos(assentos):
    garantir_pasta()
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(assentos, f, ensure_ascii=False, indent=4)

def init_sala(assentos, sala_num, linhas, colunas):
    if sala_num not in assentos:
        m = {}
        for r in range(linhas):
            letra = chr(ord('A') + r)
            for c in range(1, colunas+1):
                m[f"{letra}{c}"] = False  # False = livre
        assentos[sala_num] = m

def gerar_mapa(assentos_sala):
    linhas = sorted({code[0] for code in assentos_sala})
    colunas = sorted({int(code[1:]) for code in assentos_sala})
    mapa = []
    for letra in linhas:
        row = []
        for num in colunas:
            key = f"{letra}{num}"
            row.append("XX" if assentos_sala.get(key) else key)
        mapa.append(row)
    return mapa


# FALTA REESCREVER O CÓDIGO PARA SE ADAPTAR AS ROTAS COM FLASK