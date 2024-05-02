import socket


def cliente_raw(ip_servidor, porta_servidor):
    # Socket do cliente UDP RAW
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RDP)

    print("\n* Você está dentro do cliente RAW *")

    while True:
        print("\nSelecione uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")

        escolha = input("Digite sua escolha (1-4): ")

    # TODO
