""" drivers = [

    {
        "nome": "Fernando Souza",
        "bairro": "Pernambués",
        "turno": "AM"
    },

    {
        "nome": "Eliane Ferreira",
        "bairro": "Pituba",
        "turno": "PM"
    }

]

print (f"O motorista {drivers[0]["nome"]} foi escalado para trabalho hoje.")

# print (drivers[0]["nome"]) """

drivers = []

while True:                        # laço principal
    consulta_adcao = int(input(
        "Olá, o que você gostaria de realizar hoje? "
        "1 - Consultar Motoristas cadastrados. "
        "2 - Adcionar Novo Motorista. "
        "3 - Encerrar Programa! \n"
    ))

    if consulta_adcao not in (1, 2, 3):
        print("Opção inválida, tente novamente.")
        continue                 # volta ao começo do while

    if consulta_adcao == 3:
        break                    # agora é válido, pois estamos dentro de um while

    print("OK")
    # …trata as outras opções…

print("Fim do programa")