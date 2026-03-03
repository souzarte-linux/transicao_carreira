valor_refrigerante = 5
valor_salgado = 3
valor_doce = 2

print(valor_salgado + valor_doce)

print(type(valor_doce))

quant_refri = input("Informe a quantidade de refrigerantes: ")

quant_doce = input("Informe a quantidade de doces: ")

quant_salgado = input("Informe a quantidade de salgados: ")


print("O valor total a ser pago é: R$ " + str((valor_refrigerante * int(quant_refri)) + (valor_doce * int(quant_doce)) + (valor_salgado * int(quant_salgado))))

