""" def dar_boas_vindas (nome, sobrenome, curso):
    print ("Olá ", nome, sobrenome)
    print ("Bem Vindo ao ", curso)

dar_boas_vindas ("Fernando", "Souza", "Python") """


def dia_trabalho ():

    dias_semana = ("Segunda-feira", "Terça-feira", "Quarta-feira")
    
    turnos = ("AM", "PM")

    escala_motoristas = [
        {"nome": "Fernando", "bairro": "Pernambúes", "dia_semana": dias_semana[1], "turno": turnos[0]},
        {"nome": "Eliane", "bairro": "Pituba", "dia_semana":dias_semana[2], "turno": turnos[0] }
    ]

    print ("\n==================================================")
    print ("|              Bem Vindo ao Sistema:               |")
    print ("===================================================\n")


    while True:

        print ("\nO que deseja fazer hoje? Escolha uma das opções: \n")

        print ("    1 - Consultar Motoristas Cadastrados ")
        print ("    2 - Cadastrar novo Motorista ")
        print ("    3 - Excluir um motorista registrado ")
        print ("    4 - Fechar Programa! \n")
        
        try: 
            opcao = int(input("Escolha uma das opções: "))
        except ValueError:
            print("Digite um valor válido entre 1 a 4.")
            continue

        if opcao == 1:
            print (f"Os motoristas cadastrados são: ")
            for indice, nome in enumerate (escala_motoristas, start=1):
                print (f"{nome}")
        
        elif opcao == 2:
            nome = input("Nome: ")
            bairro_novo = input("Bairro: ")
            dia = input("Dia: ")
            turno_novo = input("Turno: ")

        escala_motoristas.append({
            "nome": nome,
            "bairro": bairro_novo,
            "dia_escalado": dia,
            "turno": turno_novo
        })



     

    



dia_trabalho()