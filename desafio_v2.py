import textwrap

def menu():
    menu_opcoes = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_opcoes)).lower()


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\nDepósito de R$ {valor:.2f} concluído com sucesso! Dinheiro na conta. ====")
    else:
        print("\n@@@ Operação de depósito falhou! O valor inserido não é válido. Tente novamente com um número positivo. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    saldo_insuficiente = valor > saldo
    limite_excedido = valor > limite
    saques_esgotados = numero_saques >= limite_saques

    if saldo_insuficiente:
        print("\n@@@ Saque não realizado! Você não possui saldo suficiente para esta transação. @@@")

    elif limite_excedido:
        print(f"\n@@@ Saque não realizado! O valor excede seu limite de R$ {limite:.2f} por operação. @@@")

    elif saques_esgotados:
        print(f"\n@@@ Saque não realizado! Você atingiu o limite máximo de {limite_saques} saques diários. Tente novamente amanhã! @@@")

    elif valor <= 0:
        print("\n@@@ Saque não realizado! O valor informado é inválido. Por favor, insira um valor positivo. @@@")

    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque de R$ {valor:.2f} efetuado com sucesso! Restam {limite_saques - numero_saques} saques hoje. ===")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n============== SEU EXTRATO ==============")
    print("Nenhuma transação foi registrada." if not extrato else extrato.strip())
    print(f"\nSaldo atual disponível:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf_digitado = input("Informe o CPF (apenas números): ")
    usuario_existente = filtrar_usuario(cpf_digitado, usuarios)

    if usuario_existente:
        print("\n@@@ Oh não! Já existe um usuário cadastrado com este CPF. @@@")
        return

    nome_completo = input("Digite o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco_completo = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ")

    usuarios.append({"nome": nome_completo, "data_nascimento": data_nascimento, "cpf": cpf_digitado, "endereco": endereco_completo})

    print("\n=== Novo usuário cadastrado com sucesso! Bem-vindo! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_encontrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_encontrados[0] if usuarios_encontrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf_usuario = input("Informe o CPF do usuário para associar à conta: ")
    usuario_vinculado = filtrar_usuario(cpf_usuario, usuarios)

    if usuario_vinculado:
        print("\n=== Conta criada com sucesso e vinculada ao usuário! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario_vinculado}

    print("\n@@@ Usuário não encontrado. Não foi possível criar a conta. @@@")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta foi cadastrada até o momento. @@@")
        return

    for conta in contas:
        detalhes_conta = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(detalhes_conta))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao_selecionada = menu()

        if opcao_selecionada == "d":
            try:
                valor_deposito = float(input("Digite o valor para depósito: "))
                saldo, extrato = depositar(saldo, valor_deposito, extrato)
            except ValueError:
                print("\n@@@ Entrada inválida para o depósito. Por favor, digite um valor numérico. @@@")

        elif opcao_selecionada == "s":
            try:
                valor_saque = float(input("Digite o valor que deseja sacar: "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor_saque,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print("\n@@@ Entrada inválida para o saque. Por favor, digite um valor numérico. @@@")

        elif opcao_selecionada == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao_selecionada == "nu":
            criar_usuario(usuarios)

        elif opcao_selecionada == "nc":
            proximo_numero_conta = len(contas) + 1
            nova_conta = criar_conta(AGENCIA, proximo_numero_conta, usuarios)

            if nova_conta:
                contas.append(nova_conta)

        elif opcao_selecionada == "lc":
            listar_contas(contas)

        elif opcao_selecionada == "q":
            print("\nObrigado por utilizar nosso sistema bancário. Esperamos vê-lo novamente em breve!")
            break

        else:
            print("\n@@@ Opção inválida! Por favor, escolha uma das opções listadas no menu. @@@")


main()
