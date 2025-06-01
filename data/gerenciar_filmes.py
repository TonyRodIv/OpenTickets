import json
import os
from data.gerenciar_sala import carregar_salas # Importa para validar salas

ARQUIVO_FILMES = os.path.join('data', 'temp', 'filmes.json')

def garantir_pasta(arquivo):
    pasta = os.path.dirname(arquivo)
    os.makedirs(pasta, exist_ok=True)

def carregar_json(arquivo):
    garantir_pasta(arquivo)
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Retorna lista vazia se o arquivo for inválido ou vazio
    return []

def salvar_json(objetos, caminho_do_arquivo): # Mudei o nome do parâmetro para clarear
    garantir_pasta(caminho_do_arquivo) # Use o parâmetro
    with open(caminho_do_arquivo, 'w', encoding='utf-8') as f: # <--- AQUI ESTÁ A MUDANÇA
        json.dump(objetos, f, ensure_ascii=False, indent=4)

def carregar_filmes():
    return carregar_json(ARQUIVO_FILMES)

def adicionar_filme_web(titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas):
    filmes = carregar_json(ARQUIVO_FILMES)
    salas_cadastradas = carregar_salas()

    # Validações
    if not titulo:
        return False, "❌ O título do filme é obrigatório."
    if any(f['titulo'].lower() == titulo.lower() for f in filmes):
        return False, f"❌ Filme '{titulo}' já existe."
    try:
        duracao_int = int(duracao)
        if duracao_int <= 0:
            return False, "❌ A duração deve ser um número positivo."
    except ValueError:
        return False, "❌ A duração deve ser um número."
    if not classificacao:
        return False, "❌ A classificação etária é obrigatória."
    if not genero:
        return False, "❌ O gênero é obrigatório."
    if not salas_escolhidas:
        return False, "❌ Selecione pelo menos uma sala."

    numeros_salas_cadastradas = [s['numero'] for s in salas_cadastradas]

    for s_id in salas_escolhidas:
        if s_id not in numeros_salas_cadastradas:
            return False, f"❌ Sala {s_id} não cadastrada."

    # Adiciona filme
    novo_filme = {
        "titulo": titulo,
        "duracao": duracao_int,
        "classificacao": classificacao,
        "genero": genero,
        "urlFoto": urlFoto or "", # Garante que seja string vazia se None
        "salas": salas_escolhidas
    }
    filmes.append(novo_filme)
    salvar_json(filmes, ARQUIVO_FILMES)
    return True, f"✅ Filme '{titulo}' adicionado com sucesso!"

def buscar_filme_por_titulo(titulo):
    filmes = carregar_json(ARQUIVO_FILMES)
    for filme in filmes:
        if filme['titulo'].lower() == titulo.lower():
            return filme
    return None

def editar_filme(titulo_original, dados_novos):
    filmes = carregar_json(ARQUIVO_FILMES)
    salas_todas = carregar_salas()
    filme_para_editar = buscar_filme_por_titulo(titulo_original)

    novo_titulo = dados_novos['titulo'].strip()
    salas_escolhidas = dados_novos.get('salas', [])

    # Valida se o novo título já existe (e não é o filme atual)
    if novo_titulo.lower() != filme_para_editar['titulo'].lower():
        if buscar_filme_por_titulo(novo_titulo):
            return False, f"Já existe um filme com o título '{novo_titulo}'."

    # Valida se as salas escolhidas existem
    numeros_salas_existentes = {s['numero'] for s in salas_todas}
    for s_id in salas_escolhidas:
        if s_id not in numeros_salas_existentes:
            return False, f"A Sala {s_id} não existe."
        # for f in filmes:
        #     if f['titulo'].lower() != filme_para_editar['titulo'].lower() and s_id in f.get('salas', []):
        #          return False, f"A Sala {s_id} já está ocupada por outro filme."

    # Atualiza os dados
    filme_para_editar['titulo'] = novo_titulo
    filme_para_editar['duracao'] = int(dados_novos['duracao'])
    filme_para_editar['classificacao'] = dados_novos['classificacao'].strip()
    filme_para_editar['genero'] = dados_novos['genero'].strip()
    filme_para_editar['salas'] = salas_escolhidas

    salvar_json(filmes, ARQUIVO_FILMES)
    return True, filme_para_editar