"""

Objetivo do desafio
Criar um programa que permita:


1 - Registrar dia de entrega    # def registrar_entrega():
2 - Listar registros            # def listar_entregas():
3 - Calcular ganhos do dia      # def calcular_ganho():
4 - Cadastro Motorista          # def cadastro_motorista():
5 - Sair

"""

def cadastro_motorista():
    
    # criar um tupla com os nomes dos bairros para entregas.
    bairros = ("Pernambués", "Pituba", "Barra", "Saramandaia", "Cabula")


    # criar um tupla com os nomes dos turnos de entregas.
    turnos = ("AM", "PM")

    # criar uma lista de dicionários com os nomes dos motoristas e seus respectivos  bairros para entregas.
    motorista = [
        {
            "nome": "Fernando",
            "bairro": bairros[0],
            "turno": turnos[0]
        }
    ]

    print (f"O motorista {motoris[nome]} está escalado para o {motorista.(bairros)} no {turno}"))

cadastro_motorista ()
