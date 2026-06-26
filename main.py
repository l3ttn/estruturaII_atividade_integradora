from tabulate import tabulate
from collections import deque
from datetime import datetime

ocorrencias = deque()
fila_atendimento = deque()
historico_acoes = []
backup_ultima_acao = [(0, 0)]

def gerencia_historico_acoes():
    while True:
        print("\n===== HISTÓRICO DE AÇÕES =====")
        print("1 - Listar Histórico de ações")
        print("2 - Desfazer última ação")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_historico_acoes()
        elif opcao == "2":
            desfazer_ultima_acao()
        elif opcao == "0":
            print("Saindooooo...")
            break
        else:
            print("Opção inválida.")

def registrar_acao(dados, tipo):
    ## Dicionário Tipos
    acoes = {
        0: "Cadastro",
        1: "Atendimento Básico",
        2: "Atendimento Prioritário",
        3: "Ação desfeita"
    }
    historico_acoes.append({
    'id': dados["id_ocorrencia"],
    'acao': acoes[tipo],
    'tipo': tipo
    })

def desfazer_ultima_acao():
    ## Dicionário Tipos
    ## 0 - Cadastrar Ocorrência
    ## 1 - Atendimento por ordem de chegada
    ## 2 - Atendimento por prioridade
    if not historico_acoes:
       return print("Histórico vazio")
    acao = historico_acoes.pop()
    tipo = acao["tipo"]
    ultima_acao, ultimo_tipo = backup_ultima_acao.pop()
    if tipo == 0:
        ocorrencia = ocorrencias.pop()
        backup_ultima_acao.append((ocorrencia, tipo))
        registrar_acao(ocorrencia, 3)
    if tipo == 1:
        ocorrencia = ocorrencias[0]
        ocorrencia["status"] = "Aberto"
        fila_atendimento.appendleft(ocorrencia)
        backup_ultima_acao.append((ocorrencia, tipo))
        registrar_acao(ocorrencia, 3)
    if tipo == 2:
        return
    if tipo == 3:
       if ultimo_tipo == 0:
           ocorrencias.append(ultima_acao)
           backup_ultima_acao.append((ultima_acao, ultimo_tipo))
           registrar_acao(ultima_acao, ultimo_tipo)
           return
       if ultimo_tipo == 1:
            ocorrencia = ocorrencias[0]
            ocorrencia["status"] = "Fechado"
            fila_atendimento.popleft()
            backup_ultima_acao.append((ultima_acao, ultimo_tipo))
            registrar_acao(ultima_acao, ultimo_tipo)      

def atender_ocorrencia_fila():
    resultado = fila_atendimento.popleft()
    resultado["status"] = "Fechado"
    registrar_acao(resultado, 1)
    print(resultado)

hash_nome = []
hash_tipo = []

for i in range(10):
    hash_nome.append([])
    hash_tipo.append([])

def djb2(chave_str, tamanho):
    hash_val = 5381
    for char in chave_str:
        hash_val = ((hash_val << 5) + hash_val) + ord(char)
    return hash_val % tamanho

def inserir_hash(tabela, chave, ocorrencia):
    posicao = djb2(chave, 10)
    tabela[posicao].append((chave, ocorrencia))

def buscar_hash(tabela, chave):
    posicao = djb2(chave, 10)
    resultados = []
    for chave_salva, oc in tabela[posicao]:
        if chave_salva == chave:
            resultados.append(oc)
    return resultados

heap = []

def subir(i):
    pai = (i - 1) // 2
    while i > 0 and int(heap[i]['prioridade']) > int(heap[pai]['prioridade']):
        heap[i], heap[pai] = heap[pai], heap[i]
        i = pai
        pai = (i - 1) // 2

def descer(i):
    tamanho = len(heap)
    while True:
        maior = i
        esq = 2 * i + 1
        drt = 2 * i + 2
        if esq < tamanho and int(heap[esq]['prioridade']) > int(heap[maior]['prioridade']):
            maior = esq
        if drt < tamanho and int(heap[drt]['prioridade']) > int(heap[maior]['prioridade']):
            maior = drt
        if maior != i:
            heap[i], heap[maior] = heap[maior], heap[i]
            i = maior
        else:
            break

def inserir_heap(ocorrencia):
    heap.append(ocorrencia)
    subir(len(heap) - 1)

def extrair_max():
    if len(heap) == 0:
        return None
    maximo = heap[0]
    heap[0] = heap[len(heap) - 1]
    heap.pop()
    if len(heap) > 0:
        descer(0)
    return maximo

raiz = None

def criar_no(chave, dado):
    return {'chave': chave, 'dado': dado, 'esq': None, 'drt': None}

def inserir_arvore(no, chave, dado):
    if no is None:
        return criar_no(chave, dado)
    if chave < no['chave']:
        no['esq'] = inserir_arvore(no['esq'], chave, dado)
    elif chave > no['chave']:
        no['drt'] = inserir_arvore(no['drt'], chave, dado)
    return no

def buscar_arvore(no, chave):
    if no is None:
        return None
    if chave == no['chave']:
        return no['dado']
    elif chave < no['chave']:
        return buscar_arvore(no['esq'], chave)
    else:
        return buscar_arvore(no['drt'], chave)

def gerar_id(nome):
    soma = 0

    for letra in nome:
        soma = soma + ord(letra)

    codigo = soma % 10000
    prefixo = nome[:3].upper()

    return prefixo + "-" + str(codigo)


def cadastrar_ocorrencia():
    print("\nCADASTRAR OCORRÊNCIA")

    nome = input("Nome do requisitante: ")
    id_ocorrencia = gerar_id(nome)

    tipo = input("Tipo da ocorrência: ")
    descricao = input("Descrição: ")
    prioridade = input("Prioridade de 1 a 5: ")
    data = datetime.now()
    print("\nOcorrência cadastrada!")
    print("ID:", id_ocorrencia)
    print("Nome:", nome)
    print("Tipo:", tipo)
    print("Descrição:", descricao)
    print("Prioridade:", prioridade)
    nova_ocorrencia = {
        'id_ocorrencia': id_ocorrencia,
        'nome': nome,
        'tipo': tipo,
        'descricao': descricao,
        'prioridade': prioridade,
        'status': "Aberto",
        'data': data
    }
    ocorrencias.append(nova_ocorrencia)
    fila_atendimento.append(nova_ocorrencia)
    registrar_acao(nova_ocorrencia, 0)

    inserir_hash(hash_nome, nome, ocorrencias[-1])
    inserir_hash(hash_tipo, tipo, ocorrencias[-1])
    inserir_heap(nova_ocorrencia)

    global raiz
    raiz = inserir_arvore(raiz, id_ocorrencia, nova_ocorrencia)

    print("Ocorrência salva com sucesso.")

def listar_historico_acoes():
    print(tabulate(historico_acoes, headers="keys", tablefmt="grid"))

def listar_ocorrencias():  
    print("\nLISTAR OCORRÊNCIAS")
    print("Aqui serão listadas as ocorrências cadastradas.")
    print(tabulate(ocorrencias, headers="keys", tablefmt="grid"))

def buscar_ocorrencia():
    print("\nBUSCAR OCORRÊNCIA POR ID")
    id_busca = input("Digite o ID para buscar: ").strip().upper()
    resultado = buscar_arvore(raiz, id_busca)
    if resultado:
        print("\nOcorrência encontrada:")
        print(tabulate([resultado], headers="keys", tablefmt="grid"))
    else:
        print("Ocorrência não encontrada.")

def atender_prioridade():
    resultado = extrair_max()
    if resultado is None:
        print("\nNenhuma ocorrência para atender.")
        return
    print("\nAtendendo ocorrência crítica:")
    resultado["status"] = "Fechado"
    print("ID:", resultado['id_ocorrencia'], "|", resultado['nome'], "|", resultado['tipo'], "| Prioridade:", resultado['prioridade'], resultado['status'])
    registrar_acao(resultado, 2)

def busca_nome_tipo():
    print("\nBUSCAR POR NOME OU TIPO")
    print("1 - Buscar por nome")
    print("2 - Buscar por tipo")
    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input("Digite o nome: ")
        resultados = buscar_hash(hash_nome, nome)
    elif opcao == "2":
        tipo = input("Digite o tipo: ")
        resultados = buscar_hash(hash_tipo, tipo)
    else:
        print("Opção inválida.")
        return

    if resultados:
        print("\nOcorrências encontradas:")
        print(tabulate(resultados, headers="keys", tablefmt="grid"))
    else:
        print("Nenhuma ocorrência encontrada.")

def menu_ordena_ocorrencias():
    while True:
        print("\nOrdenar Por:")
        print("1 - ID")
        print("2 - Prioridade")
        print("3 - Nome")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")
        busca = ''
        if opcao == "1":
            busca = 'id_ocorrencia'
        elif opcao == "2":
            busca = 'prioridade'
        elif opcao == "3":
            busca = 'nome'
        elif opcao == "0":
            return
        else:
            print("Opção inválida")
            continue
        return ordena_ocorrencias(busca)

def ordena_ocorrencias(parametro):
    n = len(ocorrencias)
    if parametro == 'prioridade':
        for i in range(n):
            for j in range(0, n-i-1):
                if ocorrencias[j][parametro] < ocorrencias[j+1][parametro]:
                    ocorrencias[j], ocorrencias[j+1] = ocorrencias[j+1], ocorrencias[j]
    else:
        for i in range(n):
            for j in range(0, n-i-1):
                if ocorrencias[j][parametro] > ocorrencias[j+1][parametro]:
                    ocorrencias[j], ocorrencias[j+1] = ocorrencias[j+1], ocorrencias[j]
    return listar_ocorrencias()

## Remover, dados temporarios
def popular_db():
    global raiz
    dados = [
        ("Maria Silva",      "Iluminação",   "Poste apagado na Rua Andrade Neves",          "3"),
        ("João Pereira",     "Buraco",       "Buraco grande na Av. Bento Gonçalves",        "4"),
        ("Ana Souza",        "Lixo",         "Acúmulo de lixo na esquina do mercado",       "2"),
        ("Carlos Oliveira",  "Vazamento",    "Vazamento de água na calçada",                "5"),
        ("Fernanda Lima",    "Iluminação",   "Lâmpada queimada na praça central",           "1"),
        ("Roberto Alves",    "Sinalização",  "Placa de pare derrubada no cruzamento",       "4"),
        ("Patrícia Gomes",   "Buraco",       "Calçada quebrada em frente à escola",         "3"),
        ("Lucas Martins",    "Vazamento",    "Esgoto a céu aberto na Rua XV",               "5"),
        ("Juliana Costa",    "Lixo",         "Entulho abandonado no terreno baldio",        "2"),
        ("Eduardo Rocha",    "Sinalização",  "Semáforo com defeito na Praça da Bandeira",   "5"),
    ]

    for nome, tipo, descricao, prioridade in dados:
        id_ocorrencia = gerar_id(nome)
        ocorrencia = {
            'id_ocorrencia': id_ocorrencia,
            'nome': nome,
            'tipo': tipo,
            'descricao': descricao,
            'prioridade': int(prioridade),
            'status': "Aberto",
            'data': datetime.now()
        }
        ocorrencias.append(ocorrencia)
        fila_atendimento.append(ocorrencia)
        inserir_hash(hash_nome, nome, ocorrencias[-1])
        inserir_hash(hash_tipo, tipo, ocorrencias[-1])
        inserir_heap(ocorrencia)
        registrar_acao(ocorrencia, 0)
        raiz = inserir_arvore(raiz, id_ocorrencia, ocorrencia)

## Remover chamada dados temporarios
popular_db()


while True:
    print("\n===== MENU =====")
    print("1 - Cadastrar ocorrência")
    print("2 - Listar ocorrências")
    print("3 - Atender próxima ocorrência pela fila")
    print("4 - Atender por prioridade")
    print("5 - Buscar ocorrência por ID")
    print("6 - Buscar por nome ou tipo")
    print("7 - Ordenar ocorrências")
    print("8 - Ver histórico de ações")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_ocorrencia()
    elif opcao == "2":
        listar_ocorrencias()
    elif opcao == "3":
        atender_ocorrencia_fila()
    elif opcao == "4":
        atender_prioridade()
    elif opcao == "5":
        buscar_ocorrencia()
    elif opcao == "6":
        busca_nome_tipo()
    elif opcao == "7":
        menu_ordena_ocorrencias()
    elif opcao == "8":
        gerencia_historico_acoes()
    elif opcao == "9":
        desfazer_ultima_acao()
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")