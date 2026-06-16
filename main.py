from tabulate import tabulate

ocorrencias = []
atendimentos = []
historico_ocorrencias = []
historico_atendimentos = []

def gerencia_historico_acoes():
    while True:
        print("\n===== HISTÓRICO =====")
        print("1 - Listar ocorrências")
        print("2 - Listar atendimentos")
        print("3 - Desfazer última ocorrência")
        print("4 - Desfazer último atendimento")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_ocorrencias()
        elif opcao == "2":
            listar_atendimentos()
        elif opcao == "3":
            desfazer_ultima_acao(historico_ocorrencias)
        elif opcao == "4":
            desfazer_ultima_acao(historico_atendimentos)    
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def desfazer_ultima_acao(pilha):
    if pilha:
        resultado = pilha.pop()
        print(tabulate(ocorrencias, headers="keys", tablefmt="grid"))
        print(f"Ocorrência apagada:\n {tabulate([resultado], headers="keys", tablefmt="grid")}")
    else:
        print("Histórico vazio")
        return


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
    tabela[posicao].append(ocorrencia)

def buscar_hash(tabela, chave):
    posicao = djb2(chave, 10)
    return tabela[posicao]

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

    print("\nOcorrência cadastrada!")
    print("ID:", id_ocorrencia)
    print("Nome:", nome)
    print("Tipo:", tipo)
    print("Descrição:", descricao)
    print("Prioridade:", prioridade)
    ocorrencia = {
        'id_ocorrencia': id_ocorrencia,
        'nome': nome,
        'tipo': tipo,
        'descricao': descricao,
        'prioridade': prioridade
    }
    ocorrencias.append(ocorrencia)
    historico_ocorrencias.append(ocorrencia)

    inserir_hash(hash_nome, nome, ocorrencias[-1])
    inserir_hash(hash_tipo, tipo, ocorrencias[-1])

    print("Ocorrência salva com sucesso.")


def listar_atendimentos():
    print("\nLISTAR ATENDIMENTOS")
    print("Aqui serão listados os atendimentos.")
    print(tabulate(atendimentos, headers="keys", tablefmt="grid"))

def listar_ocorrencias():  
    print("\nLISTAR OCORRÊNCIAS")
    print("Aqui serão listadas as ocorrências cadastradas.")
    print(tabulate(ocorrencias, headers="keys", tablefmt="grid"))

def buscar_ocorrencia():
    print("\nBUSCAR OCORRÊNCIA")
    id_busca = input("Digite o ID para buscar: ")
    print("Buscando ocorrência com ID:", id_busca)


while True:
    print("\n===== MENU =====")
    print("1 - Cadastrar ocorrência")
    print("2 - Listar ocorrências")
    print("3 - Buscar ocorrência")
    print("8 - Ver histórico de ações")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_ocorrencia()
    elif opcao == "2":
        listar_ocorrencias()
    elif opcao == "3":
        buscar_ocorrencia()
    elif opcao == "8":
        gerencia_historico_acoes()
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")