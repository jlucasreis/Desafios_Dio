menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        try:
            valor = float(input("Informe o valor do depósito: "))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido. Tente novamente com um valor positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número para o valor do depósito.")


    elif opcao == "s":
        try:
            valor = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente!")
            elif excedeu_limite:
                print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
            elif excedeu_saques:
                print(f"Operação falhou! Número máximo de saques ({LIMITE_SAQUES}) excedido. Volte amanhã!")
            elif valor <= 0:
                print("Operação falhou! O valor informado é inválido. Digite um valor positivo para sacar.")
            else:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso. Saques restantes: {LIMITE_SAQUES - numero_saques}")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número para o valor do saque.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print(f"{'Não foram realizadas movimentações.' if not extrato else extrato.strip()}")
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        print("Obrigada por usar o nosso sistema bancário. Volte sempre!")
        break

    else:
        print("Operação inválida! Por favor, selecione novamente a operação desejada.")