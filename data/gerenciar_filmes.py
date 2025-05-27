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

def salvar_json(objetos, arquivo):
    garantir_pasta(arquivo)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(objetos, f, ensure_ascii=False, indent=4)

def carregar_filmes():
    """Carrega a lista de filmes do arquivo JSON."""
    return carregar_json(ARQUIVO_FILMES)

def adicionar_filme_web(titulo, duracao, classificacao, genero, urlFoto, salas_escolhidas):
    """
    Adiciona um novo filme a partir de dados web.
    Retorna (True, 'Mensagem de sucesso') ou (False, 'Mensagem de erro').
    """
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
        # Verifica se a sala já está ocupada por *outro* filme
        if any(s_id in f.get('salas', []) for f in filmes):
            return False, f"❌ Sala {s_id} já está ocupada por outro filme."

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

def listar_filmes():
    """Carrega e retorna a lista completa de filmes."""
    return carregar_json(ARQUIVO_FILMES)

# def remover_filme():
#     print("=== Remover Filme ===")
#     listar_filmes()
#     if not filmes:
#         return

#     titulo = input("Título do filme a remover: ").strip()
#     antes  = len(filmes)
#     filmes[:] = [f for f in filmes if f['titulo'].lower() != titulo.lower()]

#     if len(filmes) < antes:
#         salvar_json(filmes, ARQUIVO_FILMES)
#         print(f"✅ Filme '{titulo}' removido.")
#     else:
#         print(f"❌ Filme '{titulo}' não encontrado.")


# def editar_filme():
#     print("=== Editar Filme ===")
#     listar_filmes()
#     if not filmes:
#         return

#     titulo = input("Título do filme a editar: ").strip()
#     for f in filmes:
#         if f['titulo'].lower() == titulo.lower():
  
#             novo_titulo = input(f"Título (atual: {f['titulo']}): ").strip() or f['titulo']
#             if novo_titulo.lower() != f['titulo'].lower() and \
#                any(x['titulo'].lower() == novo_titulo.lower() for x in filmes):
#                 print(f"❌ Já existe filme com título '{novo_titulo}'.")
#                 return

#             ndur = input(f"Duração (atual: {f['duracao']}): ").strip()
#             ncla = input(f"Classif. (atual: {f['classificacao']}): ").strip()
#             ngen = input(f"Gênero (atual: {f['genero']}): ").strip()

#             salas_atual = f.get('salas', [])
#             atual_str   = ', '.join(salas_atual)
#             listar_salas()
#             inp = input(f"Salas (atual: {atual_str}) [separe por vírgula]: ").strip()
#             if inp:
#                 novas_salas = [s.strip() for s in inp.split(',') if s.strip()]
#             else:
#                 novas_salas = salas_atual

#             for s_id in novas_salas:
#                 if not any(s['numero'] == s_id for s in salas):
#                     print(f"❌ Sala {s_id} não existe.")
#                     return
                
#                 if s_id not in salas_atual and \
#                    any(s_id in x.get('salas', []) for x in filmes):
#                     print(f"❌ Sala {s_id} já está ocupada por outro filme.")
#                     return

#             f['titulo']  = novo_titulo
#             if ndur: f['duracao']= int(ndur)
#             if ncla: f['classificacao']= ncla
#             if ngen: f['genero']= ngen
#             f['salas']= novas_salas

#             salvar_json(filmes, ARQUIVO_FILMES)
#             print(f"✅ Filme '{novo_titulo}' atualizado.")
#             return

#     print(f"❌ Filme '{titulo}' não encontrado.")
    
# FALTA REESCREVER O CÓDIGO PARA SE ADAPTAR AS ROTAS COM FLASK