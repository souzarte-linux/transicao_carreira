soma = 0
contador = 0

while True:
    valor = float(input("Digite um número (ou -1 para sair):"))

    if valor == 0:
        break

    soma += valor
    contador += 1

    print("Soma total:", soma)
    print("Quantidade digitada:", contador)
