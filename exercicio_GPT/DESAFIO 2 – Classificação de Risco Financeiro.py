# DESAFIO 2 – Classificação de Risco Financeiro


faturamento_dia = int(input("Qual é o faturamento do dia? "))

custo_combustivel = int(input("Qual o custo do combustível hoje? "))

if (faturamento_dia - custo_combustivel) >= 150:
    print("Ótimo dia! O lucro do dia é de R$ ", faturamento_dia - custo_combustivel)
elif (faturamento_dia - custo_combustivel) >= 50:
    print("Dia razoável! O lucro do dia é de R$: ", faturamento_dia - custo_combustivel)
else:
    print("Dia ruim! O lucro do dia é de R$: ", faturamento_dia - custo_combustivel)