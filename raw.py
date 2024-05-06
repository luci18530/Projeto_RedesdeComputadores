import socket
import struct

from utils import gerar_identificador


def criar_payload(tipo_requisicao, identificador):
    # Cria a mensagem com base nos campos especificados
    req_res = 0  # 0000 para requisição
    req_res_and_tipo = (
        req_res | tipo_requisicao
    )  # Combina os campos de requisicao/resposta e tipo
    payload = struct.pack(
        ">BH", req_res_and_tipo, identificador
    )  # >BH -> Big-endian, 1 Byte (para o tipo e requisicao), 2 Bytes (para o identificador)
    return payload


def calcular_checksum(
    cabecalho_ip,
    porta_origem,
    porta_destino,
    comprimento,
    checksum_provisorio,
    payload,
):

    # combina o pseudo cabeçalho, cabeçalho UDP e dados
    dados_checksum = (
        cabecalho_ip
        + porta_origem
        + porta_destino
        + comprimento
        + checksum_provisorio
        + payload
    )

    # se o comprimento dos dados for ímpar, adiciona um byte zero para torná-lo par
    if len(dados_checksum) % 2 != 0:
        dados_checksum += b"\x00"

    checksum = 0
    # itera sobre os dados em pares de bytes
    for i in range(0, len(dados_checksum), 2):
        # combina pares de 2 bytes
        par_de_bytes = (dados_checksum[i] << 8) + dados_checksum[i + 1]
        # soma a par_de_bytes ao checksum
        checksum += par_de_bytes
        # se houver um carry (vai para o próximo bit mais significativo), adiciona ao checksum
        if checksum & 0xFFFF0000:
            checksum = (checksum & 0xFFFF) + 1
    # retorna o complemento de um do checksum (16 bits)
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

    checksum_provisorio = b"\x00"
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
    pass
    # TODO


def cliente_raw(ip_servidor, porta_servidor):
    porta_origem = 59155
    porta_destino = porta_servidor
    ip_origem = str(socket.gethostbyname(socket.gethostname()))
    ip_destino = ip_servidor

    print("\n* Você está dentro do cliente RAW *")

    while True:
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

        comprimento_udp = struct.pack(">H", comprimento)

        # cabecalho_ip = criar_cabecalho_ip(ip_origem, ip_destino, comprimento)

        cabecalho_ip = criar_cabecalho_ip(ip_origem, ip_destino, comprimento_udp)
        cebecalho_udp = criar_cabecalho_udp(
            porta_origem,
            porta_destino,
            ip_origem,
            ip_destino,
            comprimento,
            payload,
        )
        print(f"cabeçalho ip: {cabecalho_ip}")
        print(f"cabeçalho udp: {cebecalho_udp}")

        datagrama = cebecalho_udp + payload

        # envia o pacote UDP
        socket_cliente = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP
        )

        print(f"datagrama: {datagrama}")

        socket_cliente.sendto(
            datagrama,
            (ip_servidor, porta_servidor),
        )

        # recebe a resposta
        resposta, _ = socket_cliente.recvfrom(2056)
        print(f"resposta: {resposta}")

        # analisa a resposta
        # tipo_resposta, identificador, texto_resposta = analisar_resposta(resposta)
        # print(f"\nRESPOSTA RECEBIDA: \nTIPO {tipo_resposta} \nID {identificador} \n{texto_resposta}")

    # fechando o socket
    socket_cliente.close()


def main():
    # informações do servidor
    ip_servidor = "15.228.191.109"
    porta_servidor = 5000

    cliente_raw(ip_servidor, porta_servidor)


if __name__ == "__main__":
    main()
