print ("\nOlá, bom dia! Seja bem-vindo(a) ao controle de Fluxo de Caixa! \nResponda as perguntas abaixo.")

convocado = input ("Hoje você foi convocado para trabalhar? (sim/não)").lower()

if convocado.lower() not in ("sim", "s"):
    print("Que pena, hoje não tem trabalho! Aproveite seu dia!")

else:
    quantPacotes = int(input("Qual a quantidade de pacotes recebido para entregar? ")) 

    bonus_dia = int(input("Hoje haverá algum bônus? Se sim, qual o valor? Se não, digite 0. "))

    bonus_quant_pacotes = 0

    valor_diaria = 290

    valor_total_dia = 0

    if quantPacotes > 0:
        valor_pacote = valor_total_dia / quantPacotes
        if quantPacotes > 131:
            bonus_quant_pacotes = 50
        elif quantPacotes >= 121:
            bonus_quant_pacotes = 30
        elif quantPacotes >= 111:
            bonus_quant_pacotes = 10

    valor_total_dia = (valor_diaria + bonus_dia)

    valor_total_dia_com_bonus = valor_total_dia + bonus_quant_pacotes

    valor_pacote = valor_total_dia_com_bonus / quantPacotes 

    print(f"\nHoje sua diária foi de R$ {valor_total_dia_com_bonus},\nsendo que foi entregue {quantPacotes} pacotes.\nO valor pago por pacote foi de R$ {valor_pacote:.2f}.\n")
