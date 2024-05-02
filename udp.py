import socket

from utils import analisar_resposta, criar_requisicao, gerar_identificador


def cliente_udp(ip_servidor, porta_servidor):
    # Socket do cliente UDP SIMPLES
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("\n* Você está dentro do cliente UDP *")

    while True:
        print("\nSelecione uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")

        escolha = input("Digite sua escolha (1-4): ")
        identificador = gerar_identificador()

        if escolha == "1":
            # Data e hora
            tipo_requisicao = 0
        elif escolha == "2":
            # Mensagem motivacional
            tipo_requisicao = 1
        elif escolha == "3":
            # Quantidade de respostas emitidas pelo servidor
            tipo_requisicao = 2
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Escolha inválida. Tente novamente.")
            continue

        # Cria a mensagem
        requisicao = criar_requisicao(tipo_requisicao, identificador)
        # Envia a requisicao
        socket_cliente.sendto(requisicao, (ip_servidor, porta_servidor))
        # Recebe a resposta
        resposta, _ = socket_cliente.recvfrom(256)

        # Analisa a resposta
        tipo_resposta, identificador, texto_resposta = analisar_resposta(resposta)
        print(
            f"\nResposta recebida (Tipo {tipo_resposta}, ID {identificador}): {texto_resposta}"
        )
    # fechando o socket
    socket_cliente.close()
