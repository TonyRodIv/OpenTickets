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
                # Converte chaves de sala e horário para string ao carregar
                assentos_data = json.load(f)
                return {str(k_sala): {str(k_horario): v_horario for k_horario, v_horario in v_sala.items()}
                        for k_sala, v_sala in assentos_data.items()}
            except json.JSONDecodeError:
                return {} 
    return {} 

def salvar_assentos(assentos):
    garantir_pasta()
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(assentos, f, ensure_ascii=False, indent=4)

# A função init_sala agora também precisa do horário
def init_sala(assentos_globais, sala_num: str, horario: str, linhas: int, colunas: int):
    # Garante que sala_num e horario sejam string
    sala_num_str = str(sala_num) 
    horario_str = str(horario)

    if sala_num_str not in assentos_globais:
        assentos_globais[sala_num_str] = {} # Inicializa a sala se ela não existe

    if horario_str not in assentos_globais[sala_num_str]:
        m = {}
        for r in range(linhas):
            letra = chr(ord('A') + r)
            for c in range(1, colunas + 1):
                m[f"{letra}{c}"] = False  # False = livre
        assentos_globais[sala_num_str][horario_str] = m # Inicializa o horário dentro da sala

# A função gerar_mapa agora recebe os assentos para um horário específico
def gerar_mapa(assentos_horario):
    if not assentos_horario:
        return []

    linhas = sorted(list(set(code[0] for code in assentos_horario)))
    colunas = sorted(list(set(int(code[1:]) for code in assentos_horario)))
    
    mapa = []
    for letra in linhas:
        row = []
        for num in colunas:
            key = f"{letra}{num}"
            row.append("XX" if assentos_horario.get(key, False) else key) 
        mapa.append(row)
    return mapa