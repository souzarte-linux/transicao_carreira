idade = input("Digite sua idade: ")

idade = int(idade)  

""" quando eu declaro que variável com o mesmo nome dela e atribuo a ela o seu mesmo valor, ela não apenas 
converte seu valor para str para aquela linha, mas o faz para o programa inteiro. para ver a diferença, comente essa
linha e imprima o tipo dessa variável ababixo. A função int() converte a string para um número inteiro, permitindo a comparação """

print("Sua idade é: \n", idade, int(idade) >= 18)  # A função int() converte a string para um número inteiro, permitindo a comparação

print(type(idade))  # O tipo de dado é string (str)
