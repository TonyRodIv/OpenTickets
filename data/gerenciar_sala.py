import json
import os

ARQUIVO_SALAS = os.path.join('data', 'temp', 'salas.json')

def garantir_pasta():
    pasta = os.path.dirname(ARQUIVO_SALAS)
    os.makedirs(pasta, exist_ok=True)

def carregar_salas():
    garantir_pasta()
    if os.path.exists(ARQUIVO_SALAS):
        with open(ARQUIVO_SALAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_salas(salas):
    garantir_pasta()
    with open(ARQUIVO_SALAS, 'w', encoding='utf-8') as f:
        json.dump(salas, f, ensure_ascii=False, indent=4)

def adicionar_sala(linhas: int, colunas: int) -> dict:
    """
    Adiciona uma nova sala com a quantidade de linhas e colunas informada.
    Retorna o dict da sala criada ou lança ValueError em caso de validação.
    """
    # Carrega lista atualizada
    salas = carregar_salas()

    # Calcula próximo número como string
    numeros = [int(s['numero']) for s in salas if s.get('numero', '').isdigit()]
    numero = str(max(numeros) + 1) if numeros else "1"

    # Validações
    if linhas < 1:
        raise ValueError("❌ Quantidade de fileiras inválida. Deve ser >= 1.")
    if linhas > 10:
        raise ValueError("⚠️ Atenção: fileiras acima de 10 podem não ser exibidas corretamente.")
    if colunas < 1:
        raise ValueError("❌ Quantidade de poltronas inválida. Deve ser >= 1.")
    if colunas > 15:
        raise ValueError("⚠️ Atenção: poltronas acima de 15 podem não ser exibidas corretamente.")

    # Cria e salva
    nova_sala = {"numero": numero, "linhas": linhas, "colunas": colunas}
    salas.append(nova_sala)
    salvar_salas(salas)
    return nova_sala

def listar_salas():
    salas = carregar_salas()
    if not salas:
        return ["Nenhuma sala cadastrada."]
    resultado = []
    for s in salas:
        total = s['linhas'] * s['colunas']
        resultado.append(f"Sala {s['numero']} – {total} cadeiras")
    return resultado

# def editar_sala():
#     listar_salas()
#     numero = input("Sala a editar: ").strip()
#     for s in salas:
#         if s["numero"] == numero:
#             novo_cad = input(f"Novo total de linhas (atual {s['cadeiras']}): ").strip()
#             if novo_cad:
#                 s["cadeiras"] = int(novo_cad)
#             salvar_salas(salas)
#             print(f"> Sala atualizada para {numero} – {s['cadeiras']} cadeiras.")
#             return
#     print(f"> Sala {numero} não encontrada.")
