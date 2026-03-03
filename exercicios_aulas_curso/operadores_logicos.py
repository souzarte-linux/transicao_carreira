idade_minima = 14
idade_cliente = 16
acompanhado_pais = False

pode_assistir = idade_cliente >= idade_minima or acompanhado_pais == True

print("Cliente pode assistir: ", pode_assistir)