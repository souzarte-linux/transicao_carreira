total = 0

while True:
    valor = float(input("Digite um valor: "))
    
    continuar = input("Deseja continuar? (s/n)").lower()

    total += valor

    if continuar != "s":
        break

print("O Valor total digital foi: ", total) 