import socket
import struct

from utils import criar_payload, gerar_identificador, obter_ip_local


def calcular_checksum(
    cabecalho_ip,
    porta_origem,
    porta_destino,
    comprimento,
    checksum_provisorio,
    payload,
):

    # combina o pseudo cabeçalho IP, cabeçalho UDP e os dados
    dados_checksum = (
        cabecalho_ip
        + porta_origem
        + porta_destino
        + comprimento
        + checksum_provisorio
        + payload
    )

    # se o comprimento dos dados for ímpar, adiciona o byte zero para se tornar par
    if len(dados_checksum) % 2 != 0:
        dados_checksum += b"\x00"

    checksum = 0
    # itera sobre os dados em pares de bytes (2 em 2)
    for i in range(0, len(dados_checksum), 2):
        # combina os pares de 2 bytes
        par_de_bytes = (dados_checksum[i] << 8) + dados_checksum[i + 1]
        # soma o par de bytes ao checksum
        checksum += par_de_bytes
        # se houver um carry, adiciona ao checksum
        if checksum & 0xFFFF0000:
            checksum = (checksum & 0xFFFF) + 1
    # retorna o complemento de um do checksum
    return ~checksum & 0xFFFF


def criar_cabecalho_ip(ip_origem, ip_destino, comprimento_udp):
    ip_origem_int = struct.unpack("!I", socket.inet_aton(ip_origem))[0]
    ip_destino_int = struct.unpack("!I", socket.inet_aton(ip_destino))[0]

    ip_origem = struct.pack(">I", ip_origem_int)
    ip_destino = struct.pack(">I", ip_destino_int)

    byte_protocolo_transporte = struct.pack(">B", 17)

    return ip_origem + ip_destino + byte_protocolo_transporte + comprimento_udp


def criar_cabecalho_udp(
    porta_origem,
    porta_destino,
    ip_origem,
    ip_destino,
    comprimento,
    payload,
):
    porta_origem = struct.pack(">H", porta_origem)
    porta_destino = struct.pack(">H", porta_destino)
    comprimento_udp = struct.pack(">H", comprimento)

    checksum_provisorio = b"\x00"  # o checksum inicia como zero

    cabecalho_ip = criar_cabecalho_ip(ip_origem, ip_destino, comprimento_udp)

    checksum = calcular_checksum(
        cabecalho_ip,
        porta_origem,
        porta_destino,
        comprimento_udp,
        checksum_provisorio,
        payload,
    )
    checksum = struct.pack(">H", checksum)

    return porta_origem + porta_destino + comprimento_udp + checksum


def analisar_resposta(resposta):
    if len(resposta) < 4:
        raise ValueError("Resposta muito curta para ser descompactada.")
    else:
        # ignora os cabeçalhos IP e UDP
        resposta = resposta[28:]
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
                texto_resposta = str(
                    resposta_decimal
                )  # Converte para string para exibir
            else:
                texto_resposta = resposta[4 : 4 + tamanho_resposta].decode("utf-8")

    return tipo_resposta, identificador, texto_resposta


def cliente_raw(ip_servidor, porta_servidor):
    porta_origem = 59155
    porta_destino = porta_servidor
    ip_origem = obter_ip_local()
    ip_destino = ip_servidor

    while True:
        print("\n* Você está dentro do cliente RAW *")
        print("\nSeleciona uma opção: ")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. SAIR")

        escolha = input("Digite sua escolha (1-4): ")
        identificador = gerar_identificador()

        if escolha == "1":
            # dados e hora
            tipo_requisicao = 0
        elif escolha == "2":
            # mensagem motivacional
            tipo_requisicao = 1
        elif escolha == "3":
            # respostas emitidas pelo servidor
            tipo_requisicao = 2
        elif escolha == "4":
            # sair
            print("Saindo...")
            break
        else:
            print("Escolha inválida. Tente novamente.")
            continue

        payload = criar_payload(tipo_requisicao, identificador)
        comprimento = 8 + len(payload)  # 8 bytes do cabeçalho + payload

        cebecalho_udp = criar_cabecalho_udp(
            porta_origem,
            porta_destino,
            ip_origem,
            ip_destino,
            comprimento,
            payload,
        )

        datagrama = cebecalho_udp + payload

        # cria o socket cliente
        socket_cliente = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_UDP,
        )

        # envia a requisição para o servidor
        socket_cliente.sendto(datagrama, (ip_servidor, porta_servidor))

        # recebe a resposta
        resposta, _ = socket_cliente.recvfrom(2056)

        # analisa a resposta
        tipo_resposta, identificador, texto_resposta = analisar_resposta(resposta)
        print(
            f"\nResposta recebida (Tipo {tipo_resposta}, ID {identificador}): {texto_resposta}"
        )

    # fechando o socket
    socket_cliente.close()
