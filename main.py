from tabulate import tabulate

ocorrencias = []
atendimentos = []
historico_acoes = []
historico_ocorrencias = []
historico_atendimentos = []

def gerencia_historico_acoes(acao):
    while True:
        print("\n===== MENU =====")
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
    resultado = pilha.pop()
    print(f"Ocorrência apagada: {resultado}")


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

    ocorrencias.append({
        'id': id_ocorrencia,
        'nome': nome,
        'tipo': tipo,
        'descricao': descricao,
        'prioridade': prioridade
    })

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
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_ocorrencia()
    elif opcao == "2":
        listar_ocorrencias()
    elif opcao == "3":
        buscar_ocorrencia()
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")