motoristas = [
    {"nome": "Fernando", "bairro": "Pernambués"},
    {"nome":"Eliane", "bairro": "Pituba"}
]

while True:

    for motorista in motoristas:
        print (motorista)

    resposta = input ("Deseja inserir um novo registro? (s/n)").lower()

    if resposta not in ("sim", "s"):
        print("Cadastro / Consulta encerrada!")
        break
        
    print ("\n==================================================")
    print ("|          Escolha uma das Opções abaixo:          |")
    print ("===================================================\n")
   
    # capta o nome do motorista e do bairro que serão inseridos no diconário.
    nome = input ("Digite seu nome: ")
    bairro = input ("Digite o nome do bairro: ")

    # insere os dados armazenados nas variáveis acima no dicionário.
    motoristas.append((nome, bairro))