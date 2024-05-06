import random
import struct


def gerar_identificador():
    return random.randint(1, 65535)


def criar_payload(tipo_requisicao, identificador):
    # Cria a mensagem com base nos campos especificados
    req_res = 0  # 0000 para requisição
    # Combina os campos de requisicao/resposta e tipo
    req_res_and_tipo = req_res | tipo_requisicao
    # >BH -> Big-endian, 1 Byte (para o tipo e requisicao), 2 Bytes (para o identificador)
    payload = struct.pack(">BH", req_res_and_tipo, identificador)

    return payload
