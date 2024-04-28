import socket
import random
import struct

def criar_requisicao(tipo_requisicao, identificador):
    # Cria a mensagem com base nos campos especificados
    req_res = 0  # 0000 para requisição
    tipo_and_res = (req_res << 4) | tipo_requisicao  # Combina os campos de requisicao/resposta e tipo
    mensagem_requisicao = struct.pack(">BH", tipo_and_res, identificador) # >BH -> Big-endian, 1 Byte (para o tipo e requisicao), 2 Bytes (para o identificador)
    return mensagem_requisicao

def analisar_resposta(resposta):
    if len(resposta) < 4:
        raise ValueError("Resposta muito curta para ser descompactada.")

    # Descompacta os campos principais da resposta
    # Primeiro byte contem req/res e tipo e o segundo/terceiro byte contem o identificador
    tipo_and_res, identificador = struct.unpack(">BH", resposta[:3])
    req_res = (tipo_and_res & 0xF0) >> 4  # Extrai os 4 bits superiores
    tipo_resposta = tipo_and_res & 0x0F  # Extrai os 4 bits inferiores

    # Verifica se ha um campo de tamanho
    if len(resposta) >= 4:
        tamanho = resposta[3]
    else:
        tamanho = 0

    # Extrai a parte de texto da resposta se houver resposta
    if tamanho > 0 and len(resposta) >= 4 + tamanho:
        if tipo_resposta == 2:
            # Converte os bytes para um numero inteiro em formato decimal (big-endian)
            resposta_decimal = int.from_bytes(resposta[4:4 + tamanho], byteorder='big')
            texto_resposta = str(resposta_decimal)  # Converte para string para exibir
        else:
            texto_resposta = resposta[4:4 + tamanho].decode("utf-8")
    else:
        texto_resposta = "Nenhum dado retornado"

    return tipo_resposta, identificador, texto_resposta

def gerar_identificador():
    return random.randint(1, 65535)

ip_servidor = "15.228.191.109"
porta_servidor = 50000
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    print("\nBem-vindo ao sistema de requisições UDP!")
    print("Selecione uma opção:")
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
    print(f"Resposta recebida (Tipo {tipo_resposta}, ID {identificador}): {texto_resposta}")

socket_cliente.close()
