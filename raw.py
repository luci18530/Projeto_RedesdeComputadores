import socket


def calcular_checksum(pseudo_cabecalho, cabecalho_udp, tipo_requisicao):
    # Combina o pseudo cabeçalho, cabeçalho UDP e dados
    dados_checksum = pseudo_cabecalho + cabecalho_udp + tipo_requisicao

    # Se o comprimento dos dados for ímpar, adiciona um byte zero para torná-lo par
    if len(dados_checksum) % 2 != 0:
        dados_checksum += b"\x00"

    checksum = 0
    # Itera sobre os dados em pares de bytes
    for i in range(0, len(dados_checksum), 2):
        # Combina pares de 2 bytes
        par_de_bytes = (dados_checksum[i] << 8) + dados_checksum[i + 1]
        # Soma a par_de_bytes ao checksum
        checksum += par_de_bytes
        # Se houver um carry (vai para o próximo bit mais significativo), adiciona ao checksum
        if checksum & 0xFFFF0000:
            checksum = (checksum & 0xFFFF) + 1
    # Retorna o complemento de um do checksum (16 bits)
    return ~checksum & 0xFFFF


def cliente_raw(ip_servidor, porta_servidor):
    # Socket do cliente UDP RAW
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    print("\n* Você está dentro do cliente RAW *")

    while True:
        print("\nSelecione uma opção:")
        print("1. dados e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")

        escolha = input("Digite sua escolha (1-4): ")

        if escolha == "1":
            # dados e hora
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
        # Calcula o comprimento do dadosgrama (cabeçalho UDP + dados)

    # TODO
