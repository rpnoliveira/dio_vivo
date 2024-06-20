#Função para deposito
def realizar_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
    else:
        print('Operação cancelada. O valor informado é inválido.')
    return saldo, extrato

#Função para saque
def realizar_saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    passou_do_saldo = valor > saldo
    passou_do_limite_de_saque = valor > limite
    passou_do_numero_saques = numero_saques >= limite_saques

    if passou_do_saldo:
        print('Saldo insuficiente.')
    elif passou_do_limite_de_saque:
        print('Valor do saque excede o limite permitido.')
    elif passou_do_numero_saques:
        print('Limite máximo de saques alcançado.')
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        numero_saques += 1
        print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
    else:
        print('Operação cancelada. O valor informado é inválido.')
    
    return saldo, extrato

#Função para exibir extrato das movimentacoes
def exibir_extrato(saldo, /, *, extrato):
    print('\n================ EXTRATO ================')
    if extrato:
        print(extrato)
    else:
        print('Não há movimentações registradas.')
    print(f'\nSaldo atual: R$ {saldo:.2f}')
    print('==========================================')

#Função para validar se o cliente já está cadastrado
def valida_cliente(cpf, clientes):

    clientes_validados = []

    for cliente in clientes:
        if cliente['cpf'] == cpf:
            clientes_validados.append(cliente)

    #Retorna o primeiro cliente ou nada
    if clientes_validados:
        return clientes_validados[0]
    else:
        return None

#Função para cadastrar um novo cliente
def novo_cliente(clientes):
    cpf = input('Informe somente os números do CPF:')
    cliente = valida_cliente(cpf, clientes)

    if cliente:
        print('Cliente já está cadastrado na base')
        return
    
    nome = input('Informe o nome do cliente:')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa) do cliente:')
    endereco = input('Informe o endereço (logradoudo, numero, bairro, cidade-estado) do cliente:')

    clientes.append({"cpf":cpf, "nome":nome, "data_nascimento":data_nascimento, "endereco":endereco})
    print('Cliente cadastrado com sucesso!')

#Função para cadastrar uma nova conta
def cadastrar_conta(agencia, numero_da_conta, clientes, contas):
    
    #Valida se o cpf existe na lista de clientes
    cpf = input('Informe somente os números do CPF:')
    cliente = valida_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não existe, favor cadastrar um cliente.')
    else:
        conta = {"agencia":agencia, "numero_da_conta":numero_da_conta, "cliente":cliente}
        contas.append(conta)
        print('Conta criada.')

#Função para sair do programa
def sair():
    print('Encerrando o sistema bancário. Até logo!')

#Definição do menu e mapeamento das funções simulando um swtich case
menu_opcoes = {
    'd': realizar_deposito,
    's': realizar_saque,
    'e': exibir_extrato,
    'nc': novo_cliente,
    'cc': cadastrar_conta,
    'q': sair,
}

def main():
    saldo = 0  #Saldo inicial
    limite = 500  #Valor do limite máximo permitido para saques
    extrato = ""  #String para armazenar o extrato das operações
    numero_saques = 0  #Contador do número de saques feitos
    LIMITE_SAQUES = 3  #Limite máximo de saques permitidos no dia
    AGENCIA = "0001" #Numero da agencia
    clientes = [] #Lista para armazenar clientes
    contas = [] #Lista para armazenar contas

    while True:
        opcao = input('\n[d] Depositar\n[s] Sacar\n[nc] Criar Cliente\n[cc] Criar Conta\n[e] Extrato\n[q] Sair\n\n=> ').lower()
        #Verifica se opção existe no menu e chama a função correspondente
        if opcao in menu_opcoes:
            if opcao == 'd':
                valor = float(input('Informe o valor do depósito: '))
                saldo, extrato = realizar_deposito(saldo, valor, extrato)
            elif opcao == 's':
                valor = float(input('Informe o valor do saque: '))
                saldo, extrato = realizar_saque(saldo = saldo, valor = valor, extrato = extrato, limite = limite, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)
            elif opcao == 'e':
                exibir_extrato(saldo, extrato = extrato)
            elif opcao == 'nc':
                novo_cliente(clientes)
            elif opcao == 'cc':
                numero_da_conta = len(contas) +1
                conta = cadastrar_conta(AGENCIA,numero_da_conta, clientes, contas)
            elif opcao == 'q':
                sair()
                break
        else:
            print('Opção inválida. Por favor, selecione novamente.')

main()