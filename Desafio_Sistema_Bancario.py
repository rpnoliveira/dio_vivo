#Definindo variáveis iniciais do sistema bancário
saldo_atual = 0  #Saldo inicial
limite_de_saque = 500  #Valor do limite máximo permitido para saques
extrato_das_operacoes = ""  #String para armazenar o extrato das operações
numero_de_saques = 0  #Contador do número de saques feitos
limite_de_saques = 3  #Limite máximo de saques permitidos no dia

#Função para deposito
def realizar_deposito():
    global saldo_atual, extrato_das_operacoes
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo_atual += valor
        extrato_das_operacoes += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação cancelada. O valor informado é inválido.")

#Função para saque
def realizar_saque():
    global saldo_atual, extrato_das_operacoes, numero_de_saques
    valor = float(input("Informe o valor do saque: "))

    passou_do_saldo = valor > saldo_atual
    passou_do_limite_de_saque = valor > limite_de_saque
    passou_do_numero_de_saques = numero_de_saques >= limite_de_saques

    if passou_do_saldo:
        print("Saldo insuficiente.")
    elif passou_do_limite_de_saque:
        print("Valor do saque excede o limite permitido.")
    elif passou_do_numero_de_saques:
        print("Limite máximo de saques alcançado.")
    elif valor > 0:
        saldo_atual -= valor
        extrato_das_operacoes += f"Saque: R$ {valor:.2f}\n"
        numero_de_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação cancelada. O valor informado é inválido.")

#Função para exibir extrato das movimentacoes
def exibir_extrato():
    global extrato_das_operacoes, saldo_atual
    print("\n================ EXTRATO ================")
    if extrato_das_operacoes:
        print(extrato_das_operacoes)
    else:
        print("Não há movimentações registradas.")
    print(f"\nSaldo atual: R$ {saldo_atual:.2f}")
    print("==========================================")

#Função para sair do programa
def sair():
    print("Encerrando o sistema bancário. Até logo!")

#Definição do menu e mapeamento das funções simulando um swtich case
menu_opcoes = {
    'd': realizar_deposito,
    's': realizar_saque,
    'e': exibir_extrato,
    'q': sair,
}

#Loop principal
while True:
    opcao = input("n\n[d] Depositar\n[s] Sacar\n[e] Extrato\n[q] Sair\n\n=> ").lower()
    #Verifica se opção existe no menu e chama a função correspondente
    if opcao in menu_opcoes:
        menu_opcoes[opcao]()
    else:
        print("Opção inválida. Por favor, selecione novamente.")
