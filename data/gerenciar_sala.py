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
    horarios_disponiveis = []
    current_time = datetime.strptime("13:00", "%H:%M")
    end_time = datetime.strptime("00:00", "%H:%M") + timedelta(days=1)

    while len(horarios_disponiveis) < 6 and current_time < end_time:
        # Pega um horário aleatório a cada 10 minutos para não ficar em hora cheia
        minutes_to_add = random.randint(0, 6) * 10 
        proposed_time = current_time + timedelta(minutes=minutes_to_add)

        if proposed_time >= end_time:
            break 

        if horarios_disponiveis:
            last_hour = datetime.strptime(horarios_disponiveis[-1], "%H:%M")
            if proposed_time - last_hour < timedelta(hours=2):
                current_time = proposed_time + timedelta(hours=2)
                continue

        horarios_disponiveis.append(proposed_time.strftime("%H:%M"))
        current_time = proposed_time + timedelta(hours=2)

    if len(horarios_disponiveis) > 6:
        horarios_disponiveis = random.sample(horarios_disponiveis, k=random.randint(4, 6))
    elif len(horarios_disponiveis) < 4: 
        pass 

    horarios_disponiveis.sort(key=lambda x: datetime.strptime(x, "%H:%M"))

    num_horarios = random.randint(4, min(6, len(horarios_disponiveis)))
    return random.sample(horarios_disponiveis, num_horarios)


def adicionar_sala(linhas: int, colunas: int) -> dict:
    # Carrega lista atualizada
    salas = carregar_salas()

    numeros_existentes = sorted([int(s['numero']) for s in salas if s.get('numero', '').isdigit()]) #

    numero_sala_escolhido = ""

    # Verifica se há números faltando na sequência
    if numeros_existentes:
        numero_esperado = 1
        for num_existente in numeros_existentes:
            if num_existente > numero_esperado:
                numero_sala_escolhido = str(numero_esperado)
                break
            numero_esperado += 1
        
        if not numero_sala_escolhido:
            numero_sala_escolhido = str(numeros_existentes[-1] + 1)
    else:
        numero_sala_escolhido = "1"

    # Validações
    if linhas < 1:
        raise ValueError("❌ Quantidade de fileiras inválida. Deve ser >= 1.")
    if linhas > 20:
        raise ValueError("⚠️ Atenção: fileiras acima de 20 podem não ser exibidas corretamente.")
    if colunas < 1:
        raise ValueError("❌ Quantidade de poltronas inválida. Deve ser >= 1.")
    if colunas > 30:
        raise ValueError("⚠️ Atenção: poltronas acima de 30 podem não ser exibidas corretamente.")

    # Gera os horários para a nova sala
    horarios_gerados = gerar_horarios_sala()

    # Cria e salva
    nova_sala = {
        "numero": numero_sala_escolhido,
        "linhas": linhas,
        "colunas": colunas,
        "horarios": horarios_gerados # Adiciona os horários aqui!
    }
    salas.append(nova_sala)
    salas_ordenadas = sorted(salas, key=lambda s: int(s['numero']))
    salvar_salas(salas_ordenadas)
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
            if linhas > 20:
                return None, "⚠️ Atenção: fileiras acima de 20 podem não ser exibidas corretamente."
            if colunas < 1:
                return None, "❌ Quantidade de colunas inválida. Deve ser >= 1."
            if colunas > 30:
                return None, "⚠️ Atenção: colunas acima de 30 podem não ser exibidas corretamente."

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