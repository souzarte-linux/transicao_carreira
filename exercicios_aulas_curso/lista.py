
empresas = ["Shopee", "Amazon", "J&T"]

print(f"\nHoje você preseta serviço para as seguintes empresas: {empresas}\n")

escolha != 0

while escolha != 3:
     escolha = int(input("\nO que deseja realizar hoje? (1 - Listar empresas já cadastrada, 2 - Cadastrar nova empresa, 3 - Sair)\n"))

if escolha == 1:
    empresas.sort()
    print(f"As empresas cadastradas e que você presta serviço são {empresas}\n")
    
elif escolha == 2:
    novaEmpresa = ("\nDigite o nome da nova empresa que deseja cadastrar: \n")
    empresas.append(novaEmpresa)

elif escolha == 3:
    print("\nAté mais!\n")
else:
    print("\nOpção inválida, tente novamente!\n")