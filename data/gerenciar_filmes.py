import json
import os

ARQUIVO_SALAS  = os.path.join('data', 'temp', 'salas.json')
ARQUIVO_FILMES = os.path.join('data', 'temp', 'filmes.json')

def garantir_pasta(arquivo):
    pasta = os.path.dirname(arquivo)
    os.makedirs(pasta, exist_ok=True)

def carregar_json(arquivo):
    garantir_pasta(arquivo)
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_json(objetos, arquivo):
    garantir_pasta(arquivo)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(objetos, f, ensure_ascii=False, indent=4)

salas  = carregar_json(ARQUIVO_SALAS)
filmes = carregar_json(ARQUIVO_FILMES)

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def listar_salas():
    if not salas:
        print("⚠️  Nenhuma sala cadastrada.")
        return
    print("Salas:")
    for s in salas:
        print(f" • Sala {s['numero']} - {s['cadeiras']} cadeiras")


def listar_filmes():
    if not filmes:
        print("⚠️  Sem filmes cadastrados.")
        return
    print("Filmes:")
    for f in filmes:
        salas_str = ', '.join(f.get('salas', []))
        print(
            f" • {f['titulo']} | {f['duracao']}min | {f['genero']} | "
            f"Classif.: {f['classificacao']} | Salas: {salas_str}"
        )


def adicionar_filme():
    print("=== Adicionar Filme ===")
    titulo = input("Título: ").strip()
    chave  = titulo.lower()
    urlFoto = input("URL da foto (opcional): ").strip()
    if any(f['titulo'].lower() == chave for f in filmes):
        print(f"❌ Filme '{titulo}' já existe.")
        return

    duracao= int(input("Duração (min): ").strip())
    classificacao = input("Classificação etária: ").strip()
    genero= input("Gênero: ").strip()

    listar_salas()
    salas_input = input("Número(s) da(s) sala(s) (separe por vírgula): ").strip()
    salas_escolhidas = [s.strip() for s in salas_input.split(',') if s.strip()]

    for s_id in salas_escolhidas:
        if not any(s['numero'] == s_id for s in salas):
            print(f"❌ Sala {s_id} não cadastrada.")
            return

        if any(s_id in f.get('salas', []) for f in filmes):
            print(f"❌ Sala {s_id} já está ocupada por outro filme.")
            return

    filmes.append({
        "titulo":titulo,
        "duracao":duracao,
        "classificacao":classificacao,
        "genero":genero,
        "salas":salas_escolhidas
    })
    salvar_json(filmes, ARQUIVO_FILMES)
    print(f"✅ Filme '{titulo}' adicionado nas salas {', '.join(salas_escolhidas)}.")


def remover_filme():
    print("=== Remover Filme ===")
    listar_filmes()
    if not filmes:
        return

    titulo = input("Título do filme a remover: ").strip()
    antes  = len(filmes)
    filmes[:] = [f for f in filmes if f['titulo'].lower() != titulo.lower()]

    if len(filmes) < antes:
        salvar_json(filmes, ARQUIVO_FILMES)
        print(f"✅ Filme '{titulo}' removido.")
    else:
        print(f"❌ Filme '{titulo}' não encontrado.")


def editar_filme():
    print("=== Editar Filme ===")
    listar_filmes()
    if not filmes:
        return

    titulo = input("Título do filme a editar: ").strip()
    for f in filmes:
        if f['titulo'].lower() == titulo.lower():
  
            novo_titulo = input(f"Título (atual: {f['titulo']}): ").strip() or f['titulo']
            if novo_titulo.lower() != f['titulo'].lower() and \
               any(x['titulo'].lower() == novo_titulo.lower() for x in filmes):
                print(f"❌ Já existe filme com título '{novo_titulo}'.")
                return

            ndur = input(f"Duração (atual: {f['duracao']}): ").strip()
            ncla = input(f"Classif. (atual: {f['classificacao']}): ").strip()
            ngen = input(f"Gênero (atual: {f['genero']}): ").strip()

            salas_atual = f.get('salas', [])
            atual_str   = ', '.join(salas_atual)
            listar_salas()
            inp = input(f"Salas (atual: {atual_str}) [separe por vírgula]: ").strip()
            if inp:
                novas_salas = [s.strip() for s in inp.split(',') if s.strip()]
            else:
                novas_salas = salas_atual

            for s_id in novas_salas:
                if not any(s['numero'] == s_id for s in salas):
                    print(f"❌ Sala {s_id} não existe.")
                    return
                
                if s_id not in salas_atual and \
                   any(s_id in x.get('salas', []) for x in filmes):
                    print(f"❌ Sala {s_id} já está ocupada por outro filme.")
                    return

            f['titulo']  = novo_titulo
            if ndur: f['duracao']= int(ndur)
            if ncla: f['classificacao']= ncla
            if ngen: f['genero']= ngen
            f['salas']= novas_salas

            salvar_json(filmes, ARQUIVO_FILMES)
            print(f"✅ Filme '{novo_titulo}' atualizado.")
            return

    print(f"❌ Filme '{titulo}' não encontrado.")
    
# FALTA REESCREVER O CÓDIGO PARA SE ADAPTAR AS ROTAS COM FLASK