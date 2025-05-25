import json
import os
from typing import Optional, Tuple

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

def editar_sala(numero: str,linhas: int,colunas: int) -> Tuple[Optional[dict], Optional[str]]:
    """
    Atualiza linhas e colunas da sala indicada.
    Retorna (sala_atualizada, None) ou (None, mensagem_de_erro).
    """
    salas = carregar_salas()
    if not salas:
        return None, "Nenhuma sala cadastrada."
    for s in salas:
        if s["numero"] == numero:
            # Validações
            if linhas < 1:
                return None, "❌ Quantidade de fileiras inválida. Deve ser >= 1."
            if linhas > 10:
                return None, "⚠️ Atenção: fileiras acima de 10 podem não ser exibidas corretamente."
            if colunas < 1:
                return None, "❌ Quantidade de colunas inválida. Deve ser >= 1."
            if colunas > 15:
                return None, "⚠️ Atenção: colunas acima de 15 podem não ser exibidas corretamente."

            # Atualiza e salva
            s["linhas"] = linhas
            s["colunas"] = colunas
            salvar_salas(salas)
            return s, None

    return None, f"Sala {numero} não encontrada."

def deletar_sala(numero: str) -> Optional[str]:
    """
    Remove a sala indicada.
    Retorna mensagem de erro ou None se a sala foi removida com sucesso.
    """
    salas = carregar_salas()
    if not salas:
        return "Nenhuma sala cadastrada."
    for s in salas:
        if s["numero"] == numero:
            salas.remove(s)
            salvar_salas(salas)
            return None
    return f"Sala {numero} não encontrada."
