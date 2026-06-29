import time
from tabulate import tabulate
from collections import deque
from datetime import datetime

ocorrencias = deque()
fila_atendimento = deque()
historico_acoes = []

def gerencia_historico_acoes():
    while True:
        print("\n=======================================")
        print("         HISTÓRICO DE AÇÕES            ")
        print("=======================================")
        print("  1 - Listar Histórico de ações")
        print("  2 - Desfazer última ação")
        print("  0 - Voltar")
        print("=======================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_historico_acoes()
        elif opcao == "2":
            desfazer_ultima_acao()
        elif opcao == "0":
            print("\nVoltando ao menu principal...")
            time.sleep(1)
            break
        else:
            print("\n⚠️ Opção inválida.")
            time.sleep(1)

def registrar_acao(dados, tipo):
    ## Dicionário Tipos
    acoes = {
        0: "Cadastro",
        1: "Atendimento Básico",
        2: "Atendimento Prioritário",
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
       print("\n⚠️ Histórico vazio.")
       time.sleep(1.5)
       return
    acao = historico_acoes.pop()
    tipo = acao["tipo"]
    if tipo == 0:
        ocorrencias.pop()
    elif tipo == 1:
        ocorrencia = buscar_arvore(raiz, acao["id"])
        ocorrencia["status"] = "Aberto"
        fila_atendimento.appendleft(ocorrencia)
    elif tipo == 2:
        ocorrencia = buscar_arvore(raiz, acao["id"])
        ocorrencia["status"] = "Aberto"
        inserir_heap(ocorrencia)
    print(f"\n🔄 Ação desfeita com sucesso: {acao['acao']} (ID: {acao['id']})")
    time.sleep(1.5)

def atender_ocorrencia_fila():
    if not fila_atendimento:
        print("\n⚠️ Nenhuma ocorrência na fila de atendimento.")
        time.sleep(1.5)
        return
    resultado = fila_atendimento.popleft()
    resultado["status"] = "Fechado"
    registrar_acao(resultado, 1)
    print("\n=======================================")
    print("      ATENDENDO OCORRÊNCIA (FILA)      ")
    print("=======================================")
    print(tabulate([resultado], headers="keys", tablefmt="grid"))
    print("=======================================")
    time.sleep(2)

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
    print("\n=======================================")
    print("         CADASTRAR OCORRÊNCIA          ")
    print("=======================================")

    nome = input("Nome do requisitante: ")
    id_ocorrencia = gerar_id(nome)

    tipo = input("Tipo da ocorrência: ")
    descricao = input("Descrição: ")
    prioridade = input("Prioridade de 1 a 5: ")
    data = datetime.now()
    
    print("\n⌛ Processando cadastro...")
    time.sleep(1)

    print("\n✅ Ocorrência cadastrada com sucesso!")
    print(f"👉 ID Gerado: {id_ocorrencia}")
    
    nova_ocorrencia = {
        'id_ocorrencia': id_ocorrencia,
        'nome': nome,
        'tipo': tipo,
        'descricao': descricao,
        'prioridade': int(prioridade),
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

    print("💾 Gravado em todas as estruturas de dados obrigatórias.")
    time.sleep(2)

def listar_historico_acoes():
    print("\n==================================================")
    print("               HISTÓRICO DE AÇÕES                 ")
    print("==================================================")
    if not historico_acoes:
        print("Nenhuma ação registrada até o momento.")
    else:
        print(tabulate(historico_acoes, headers="keys", tablefmt="grid"))
    print("==================================================")
    input("\nPressione [ENTER] para voltar...")

def listar_ocorrencias():  
    print("\n======================================================================")
    print("                         LISTAR OCORRÊNCIAS                           ")
    print("======================================================================")
    if not ocorrencias:
        print("Não há nenhuma ocorrência cadastrada.")
    else:
        print(tabulate(ocorrencias, headers="keys", tablefmt="grid"))
    print("======================================================================")
    input("\nPressione [ENTER] para voltar...")

def buscar_ocorrencia