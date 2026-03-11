dia_semana = (
    "Domingo",
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
)

motoristas = [
    ("Fernando", dia_semana[0], "Pernambués"),
    ("Eliane", dia_semana[1], "Pituba")
]

while True:

    print("\nHoje possuímos os seguintes motoristas e seus respectivos dias:\n")

    for motorista in motoristas:
        print(motorista)

    novo_drive = input("\nVocê deseja cadastrar um novo motorista? (s/n) ").lower()

    if novo_drive not in ("s", "sim"):
        print("Cadastro / Consulta encerrada!")
        break

    print("\nDigite os dados na seguinte ordem:\n")

    nome_drive = input("Digite o nome: ")

    dia_semana_drive = int(input("Digite o dia da semana (0-5): "))

    bairro_drive = input("Digite o bairro: ")

    motoristas.append((nome_drive, dia_semana[dia_semana_drive], bairro_drive))