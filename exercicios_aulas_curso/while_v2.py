total = 0

continuar = "s"

while continuar == "s":
    valor = float(input("Digite um valor: "))
    
    continuar = input("Deseja continuar? (s/n)").lower()

    total += valor

print("O Valor total digital foi: ", total) 