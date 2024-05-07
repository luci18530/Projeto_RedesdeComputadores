import socket
import struct

from utils.utils import criar_payload, gerar_identificador


def analisar_resposta(resposta):
    if len(resposta) < 4:
        raise ValueError("Resposta muito curta para ser descompactada.")
    else:
        # Descompacta os campos principais da resposta
        # Primeiro byte contem req/res e tipo e o segundo/terceiro byte contem o identificador
        req_res_and_tipo, identificador = struct.unpack(">BH", resposta[:3])
        # Extrai os 4 bits menos significativos (tipo de resposta)
        tipo_resposta = req_res_and_tipo & 0x0F

        tamanho_resposta = resposta[3]

        if tamanho_resposta == 0:
            texto_resposta = "Nenhuma resposta (REQUISIÇÃO INVÁLIDA)"
        else:
            if tipo_resposta == 2:
                # Converte os bytes para um numero inteiro em formato decimal (big-endian)
                resposta_decimal = int.from_bytes(
                    resposta[4 : 4 + tamanho_resposta], byteorder="big"
                )
                # converte para string para exibir resposta
                texto_resposta = str(resposta_decimal)
            else:
                texto_resposta = resposta[4 : 4 + tamanho_resposta].decode("utf-8")

    return tipo_resposta, identificador, texto_resposta


def cliente_udp(ip_servidor, porta_servidor):
    while True:
        print("\n* Você está dentro do cliente UDP *")
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
        requisicao = criar_payload(tipo_requisicao, identificador)

        # cria socket udp e envia a requisição
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
