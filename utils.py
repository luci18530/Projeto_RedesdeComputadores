import random
import struct


def gerar_identificador():
    return random.randint(1, 65535)


def criar_requisicao(tipo_requisicao, identificador):
    # Cria a mensagem com base nos campos especificados
    req_res = 0  # 0000 para requisição
    req_res_and_tipo = (
        req_res | tipo_requisicao
    )  # Combina os campos de requisicao/resposta e tipo
    mensagem_requisicao = struct.pack(
        ">BH", req_res_and_tipo, identificador
    )  # >BH -> Big-endian, 1 Byte (para o tipo e requisicao), 2 Bytes (para o identificador)
    return mensagem_requisicao


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
                texto_resposta = str(
                    resposta_decimal
                )  # Converte para string para exibir
            else:
                texto_resposta = resposta[4 : 4 + tamanho_resposta].decode("utf-8")

    return tipo_resposta, identificador, texto_resposta
