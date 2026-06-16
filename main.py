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


def listar_ocorrencias():
    print("\nLISTAR OCORRÊNCIAS")
    print("Aqui serão listadas as ocorrências cadastradas.")


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