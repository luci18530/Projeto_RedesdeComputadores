import random
import socket
import struct


def gerar_identificador():
    return random.randint(1, 65535)


def obter_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        endereco_ip = s.getsockname()[0]
    except Exception:
        endereco_ip = "127.0.0.1"
    finally:
        s.close()
    return endereco_ip


def criar_payload(tipo_requisicao, identificador):
    # Cria a mensagem com base nos campos especificados
    req_res = 0  # 0000 para requisição

    # Combina os campos de requisicao/resposta e tipo
    req_res_and_tipo = req_res | tipo_requisicao

    # >BH -> Big-endian, 1 Byte (para o tipo e requisicao), 2 Bytes (para o identificador)
    payload = struct.pack(">BH", req_res_and_tipo, identificador)

    return payload
