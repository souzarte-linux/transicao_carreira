""" motoristas = [
    ("Fernando", "Pernambués", "AM"), 
     ("Eliane", "Pituba", "AM"), 
     ("Gilval", "Barra", "PM")
    ]

for nome, _, turno in motoristas:
    print (nome, turno) """


alimentos = [
    ("Fernando", "umbu", "suco"),
    ("Eliane", "uva", "inatura"),
]

while True:

    for nome, fruta, tipoingerido in alimentos:
        print (f"\n - {nome}, gosta da fruta {fruta}, e degusta da seguinte forma {tipoingerido}\n")

        
    print ("\n Responda as perguntas a seguir para cadastrar um novo gosto da família: ")

    novoNome = input ("\nQual o seu nome: \n")

    novaFruta = input ("Qual sua fruta favorita? ")

    novaForma = input ("E por fim, qual a forma de ingerir preferida? ")


    alimentos.append((novoNome, novaFruta, novaForma))