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
    with open(caminho_do_arquivo, 'w', encoding='utf-8') as f:
        json.dump(objetos, f, ensure_ascii=False, indent=4)

def carregar_filmes():
    return carregar_json(ARQUIVO_FILMES)

def adicionar_filme_web(titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas):
    filmes = carregar_json(ARQUIVO_FILMES)
    salas_cadastradas = carregar_salas()

    # Validações (talvez seja apagada por redundância  )
    if any(f['titulo'].lower() == titulo.lower() for f in filmes):
        return False, f"❌ Filme '{titulo}' já existe."

    numeros_salas_cadastradas = [s['numero'] for s in salas_cadastradas]

    for s_id in salas_escolhidas:
        if s_id not in numeros_salas_cadastradas:
            return False, f"❌ Sala {s_id} não cadastrada."

    # Adiciona filme
    novo_filme = {
        "titulo": titulo,
        "duracao": int(duracao), # Converte para inteiro
        "classificacao": classificacao,
        "genero": genero,
        "urlFoto": urlFoto or "", # Garante que seja string vazia se None
        "salas": salas_escolhidas
    }
    filmes.append(novo_filme)
    salvar_json(filmes, ARQUIVO_FILMES)
    return True, f"✅ Filme '{titulo}' adicionado com sucesso!"

def buscar_filme_por_titulo(titulo, lista_de_filmes):
    for filme in lista_de_filmes: 
        if filme['titulo'].lower() == titulo.lower():
            return filme
    return None

def editar_filme(titulo_original, dados_novos):
    filmes = carregar_json(ARQUIVO_FILMES) # <--- Carrega a lista UMA VEZ

    filme_para_editar = buscar_filme_por_titulo(titulo_original, filmes) # <--- PASSE 'filmes' AQUI!

    if not filme_para_editar:
        return False, f"Filme '{titulo_original}' não encontrado."

    novo_titulo = dados_novos['titulo'].strip()
    salas_escolhidas = dados_novos.get('salas', [])
    
    if novo_titulo.lower() != filme_para_editar['titulo'].lower():
        if buscar_filme_por_titulo(novo_titulo, filmes):
            return False, f"Já existe um filme com o título '{novo_titulo}'."

    # Atualiza os dados
    filme_para_editar['titulo'] = novo_titulo
    filme_para_editar['duracao'] = int(dados_novos['duracao'])
    filme_para_editar['classificacao'] = dados_novos['classificacao'].strip()
    filme_para_editar['genero'] = dados_novos['genero'].strip()
    filme_para_editar['salas'] = salas_escolhidas

    salvar_json(filmes, ARQUIVO_FILMES)
    return True, filme_para_editar