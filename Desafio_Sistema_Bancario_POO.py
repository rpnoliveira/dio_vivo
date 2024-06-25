from abc import ABC, abstractmethod
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print('Saldo insuficiente.')
            return False
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        else:
            print('Operação cancelada. O valor informado é inválido.')
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        else:
            print('Operação cancelada. O valor informado é inválido.')
            return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        if valor > self._limite:
            print('Valor do saque excede o limite permitido.')
            return False
        elif numero_saques >= self._limite_saques:
            print('Limite máximo de saques alcançado.')
            return False
        else:
            return super().sacar(valor)

def valida_cliente(cpf, clientes):

    clientes_validados = []

    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_validados.append(cliente)

    if clientes_validados:
        return clientes_validados[0]
    else:
        return None

def recuperar_conta(cliente):
    if not cliente.contas:
        print('Cliente não possui conta! Favor cadastrar uma conta')
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = valida_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não existe, favor cadastrar um cliente.')
        return

    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = valida_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não existe, favor cadastrar um cliente.')
        return

    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = valida_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não existe, favor cadastrar um cliente.')
        return

    conta = recuperar_conta(cliente)
    if not conta:
        return

    print('\n================ EXTRATO =============')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não há movimentações registradas.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao["tipo"]}:R$ {transacao["valor"]:.2f}'

    print(extrato)
    print(f'\nSaldo atual:R$ {conta.saldo:.2f}')
    print('=======================================')

def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente número): ')
    cliente = valida_cliente(cpf, clientes)

    if cliente:
        print('Cliente já está cadastrado na base')
        return

    nome = input('Informe o nome do cliente:')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa) do cliente:')
    endereco = input('Informe o endereço (logradoudo, numero, bairro, cidade-estado) do cliente:')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('Cliente cadastrado com sucesso!')

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = valida_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não existe, favor cadastrar um cliente.')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')

def sair(clientes, contas):
    print('Encerrando o sistema bancário. Até logo!')
    exit()

menu_opcoes = {
    'd': depositar,
    's': sacar,
    'e': exibir_extrato,
    'nc': criar_cliente,
    'cc': criar_conta,
    'q': sair,
}

def main():
    clientes = []
    contas = []
    while True:
        opcao = input('\n[d] Depositar\n[s] Sacar\n[nc] Criar Cliente\n[cc] Criar Conta\n[e] Extrato\n[q] Sair\n\n=> ').lower()

        if opcao in menu_opcoes:
            if opcao == 'cc':
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            elif opcao == 'q':
                sair(clientes, contas)
                break
            else:
                menu_opcoes[opcao](clientes)
        else:
            print('Opção inválida. Por favor, selecione novamente.')

main()