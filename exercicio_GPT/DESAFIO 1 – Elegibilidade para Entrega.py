print("Olá, seja bem-vindo ao desafio 1! Vamos verificar se você é elegível para entrega. \nPara isso, precisamos saber algumas informações. Responda as perguntas abaixo:  ")

idade = input("Digite sua idade: ")
cnh = input("Você possui CNH? (sim/não): ").strip().lower()
veiculo = input("Você possui veículo? (sim/não): ").strip().lower()

idade = int(idade)  # A função int() converte a string para um número inteiro, permitindo a comparação

if idade >= 18 and cnh == "sim" and veiculo == "sim":
    print("Parabéns! Você é elegível para entrega.")
else:
    print("Desculpe, você não é elegível para entrega.")