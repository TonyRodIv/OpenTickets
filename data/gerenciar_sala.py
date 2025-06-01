import json
import os
from typing import Optional, Tuple
import random
from datetime import datetime, timedelta

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

def gerar_horarios_sala():
    """Gera uma lista de 4 a 5 horários aleatórios para uma sala,
    entre 13h e 00h, com intervalo mínimo de 2 horas."""
    horarios_disponiveis = []
    # Começa às 13h
    current_time = datetime.strptime("13:00", "%H:%M")
    # Termina às 00h (do dia seguinte para facilitar a lógica)
    end_time = datetime.strptime("00:00", "%H:%M") + timedelta(days=1)

    # Gera horários iniciais e tenta adicionar até 5
    while len(horarios_disponiveis) < 5 and current_time < end_time:
        # Pega um horário aleatório a cada 10 minutos para não ficar em hora cheia
        minutes_to_add = random.randint(0, 5) * 10 
        proposed_time = current_time + timedelta(minutes=minutes_to_add)

        # Garante que não ultrapasse 00:00 do dia seguinte (ou seja, 24:00)
        if proposed_time >= end_time:
            break # Parar se passar da meia-noite

        # Garante intervalo mínimo de 2 horas do último horário adicionado
        if horarios_disponiveis:
            last_hour = datetime.strptime(horarios_disponiveis[-1], "%H:%M")
            if proposed_time - last_hour < timedelta(hours=2):
                current_time = proposed_time + timedelta(hours=2) # Avança para depois do intervalo
                continue # Tenta de novo a partir do novo current_time

        horarios_disponiveis.append(proposed_time.strftime("%H:%M"))
        current_time = proposed_time + timedelta(hours=2) # Avança para o próximo possível horário

    # Randomiza a quantidade entre 4 e 5, se tiver mais que 4
    if len(horarios_disponiveis) > 5:
        horarios_disponiveis = random.sample(horarios_disponiveis, k=random.randint(4, 5))
    elif len(horarios_disponiveis) < 4: # Se por algum motivo gerou menos, tentar preencher ou avisar
        # Por simplicidade, se gerou menos, a gente mantém o que tem ou pode adicionar uma lógica de re-tentativa
        pass # Por enquanto, deixa assim.

    # Ordena os horários
    horarios_disponiveis.sort(key=lambda x: datetime.strptime(x, "%H:%M"))

    # Pega apenas 4 ou 5 horários no final para garantir o número de horários
    num_horarios = random.randint(4, min(5, len(horarios_disponiveis)))
    return random.sample(horarios_disponiveis, num_horarios)


def adicionar_sala(linhas: int, colunas: int) -> dict:
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

    # Gera os horários para a nova sala
    horarios_gerados = gerar_horarios_sala()

    # Cria e salva
    nova_sala = {
        "numero": numero,
        "linhas": linhas,
        "colunas": colunas,
        "horarios": horarios_gerados # Adiciona os horários aqui!
    }
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
        horarios_str = ", ".join(s.get('horarios', [])) # Pega os horários e formata
        resultado.append(f"Sala {s['numero']} – {total} cadeiras | Horários: {horarios_str}")
    return resultado

def editar_sala(numero: str,linhas: int,colunas: int) -> Tuple[Optional[dict], Optional[str]]:
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
            # Não altera os horários existentes na edição para simplificar
            salvar_salas(salas)
            return s, None

    return None, f"Sala {numero} não encontrada."

def deletar_sala(numero: str) -> Optional[str]:
    salas = carregar_salas()
    if not salas:
        return "Nenhuma sala cadastrada."
    for s in salas:
        if s["numero"] == numero:
            salas.remove(s)
            salvar_salas(salas)
            return None
    return f"Sala {numero} não encontrada."