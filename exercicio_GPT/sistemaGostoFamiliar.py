print ("\n==================================================")
print ("|    Sistema de Gosto Familiar da Alimentação    |")
print ("==================================================\n")


alimentos = [
    ("Fernando", "Umbu", "Suco"),
    ("Eliane", "Uva", "Inatura"),
]

while True:

    print("\n1 - Listar gostos")
    print("2 - Cadastrar novo gosto")
    print("3 - Remover registro")
    print("4 - Sair")
    print("5 - Bascar gosto por nome \n")

    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Digite apenas números.")
        continue

    if opcao == 1:

      #  desempacotamento da tupla listar os nomes e respectivos gostos cadastrados.
        for i, (nome, fruta, forma) in enumerate(alimentos, start=1):
            print (f"{i} - {nome} gosta de {fruta} ({forma})")

        print ("\n==================================================")
        print ("|          Escolha uma das Opções abaixo:          |")
        print ("==================================================\n")
    
    elif opcao == 2:
        print ("\n==================================================")
        print ("|        Cadastrar novo Membro e seu Gosto:       |")
        print ("==================================================\n")

        # criação das variáveis para armazenar os novos dados dos membros
        novoNome = input ("Qual o nome do novo Membro? ")
        novaFruta = input ("Qual a nova Fruta? ")
        novaForma = input ("Qual a forma de consumo? ")

        
        #acrescentando um novo registro à lista no Python. Sendo que o primeiro parenteses se refere a lista e o segundo ao registro da Tupla.
        alimentos.append((novoNome, novaFruta, novaForma))

        #impressão do registro atualizado acima.
        print (f"\n{novoNome} gosta da fruta {novaFruta} na forma {novaForma}.")
        print ("Cadastro realizado com Sucesso!")

        print ("\n==================================================")
        print ("|          Escolha uma das Opções abaixo:          |")
        print ("==================================================\n")

    #nesse trecho será codificado a remoção de registros.
    elif opcao == 3:
        print ("\n============================================================")
        print ("|  Qual dos Registro abaixo deseja EXCLUIR PERMANENTEMENTE:   |")
        print ("==============================================================\n")

        #aqui é listado todos os registro para o usuário escolher qual registro será deletado.
        for i, (nome, fruta, forma) in enumerate(alimentos, start=1):
            print(f"{i} - {nome} gosta de {fruta}")

        #aqui é capturado o índice do membro da família que será excluído.
        excluiRegistro = int(input("\n Digite o ID para ser excluído: "))

        #aqui será validado se o valor digitado acima é um valor válido, ou seja, se está constando no registro listado acima.
        if 1 <= excluiRegistro <= len(alimentos):
            alimentos.pop(excluiRegistro - 1)
        else: #aqui apresenta mensagem de erro caso o usuário digite um número fora do intervalor cadastro no registro.
            print("Número inválido.")
    
    elif opcao == 5:
        print ("\n==================================================")
        print ("|   Digite o nome abaixo que deseja consultar:     |")
        print ("==================================================\n")

        buscarNome = input("Digite o nome para ser buscado... ")

        for nome, fruta, forma in alimentos:
            if buscarNome.lower() == nome.lower():
                print (f"\n+ {nome} gosta da fruta {fruta} na forma {forma}")
                encontrado = True # essa variável será verdadeira enquanto o nome digitado estiver na lista e poder ser impresso a mensagem acima, caso contrário apresentará a mensagem de notificação abaixo.
        
        # cria notificação ao usuário se o nome digitado não estiver na lista.
        if not encontrado:
            print ("Nome não encontrado na lista.")

    elif opcao == 4:
        print("\nEncerrando sistema...")
        break
    else:
        print ("Opção Inválida, escolha uma das opção acima.")