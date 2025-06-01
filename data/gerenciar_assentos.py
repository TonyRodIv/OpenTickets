import json, os

ARQUIVO = os.path.join('data','temp','assentos.json')

def garantir_pasta():
    pasta = os.path.dirname(ARQUIVO)
    os.makedirs(pasta, exist_ok=True)

def carregar_assentos():
    garantir_pasta()
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            try:
                # Converte chaves de sala para string ao carregar, se necessário
                assentos = json.load(f)
                return {str(k): v for k, v in assentos.items()} 
            except json.JSONDecodeError:
                return {} # Retorna dicionário vazio se o arquivo for inválido ou vazio
    return {} 

def salvar_assentos(assentos):
    garantir_pasta()
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(assentos, f, ensure_ascii=False, indent=4)

def init_sala(assentos, sala_num, linhas, colunas):
    # Garante que sala_num seja string
    sala_num_str = str(sala_num) 
    if sala_num_str not in assentos:
        m = {}
        # Gera os assentos no formato A1, A2, B1, B2...
        for r in range(linhas):
            letra = chr(ord('A') + r)
            for c in range(1, colunas + 1):
                m[f"{letra}{c}"] = False  # False = livre
        assentos[sala_num_str] = m # Usa a chave como string

def gerar_mapa(assentos_sala):
    if not assentos_sala: # Se não tiver assentos, retorna um mapa vazio
        return []

    # Extrai e ordena as linhas (letras) e colunas (números)
    linhas = sorted(list(set(code[0] for code in assentos_sala)))
    colunas = sorted(list(set(int(code[1:]) for code in assentos_sala)))
    
    mapa = []
    for letra in linhas:
        row = []
        for num in colunas:
            key = f"{letra}{num}"
            # Usa 'XX' para ocupado, o próprio código do assento para livre
            row.append("XX" if assentos_sala.get(key, False) else key) 
        mapa.append(row)
    return mapa