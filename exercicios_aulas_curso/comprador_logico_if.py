idade = input("Digite sua idade: ")

idade = int(idade) # A função int() converte a string para um número inteiro, permitindo a comparação

if idade >= 18:
    print("Adulto")
elif idade <= 12:
    print("criança")
else:
    print("Adolescente")