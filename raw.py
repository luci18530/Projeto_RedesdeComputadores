import socket
import struct
import random

def calcular_checksum(pseudo_cabecalho, cabecalho_udp, tipo_requisicao):
    #combina o pseudo cabeçalho, cabeçalho UDP e dados
    dados_checksum = pseudo_cabecalho + cabecalho_udp + tipo_requisicao

    #se o comprimento dos dados for ímpar, adiciona um byte zero para torná-lo par
    if len(dados_checksum) % 2 != 0:
        dados_checksum += b"/x00"

    checksum = 0
    #itera sobre os dados em pares de bytes
    for i in range(0, len(dados_checksum), 2):
        #combina pares de 2 bytes
        par_de_bytes = (dados_checksum[i] << 8) + dados_checksum[i + 1]
        #soma a par_de_bytes ao checksum
        checksum += par_de_bytes
        #se houver um carry (vai para o próximo bit mais significativo), adiciona ao checksum
        if checksum & 0xFFFF0000:
            checksum = (checksum & 0xFFFF) + 1
    #retorna o complemento de um do checksum (16 bits)
    return ~checksum & 0xFFFF

def create_udp_header(porta_origem: int, porta_destino: int, lenght: int, checksum: int, payload: bytes) -> bytes:

    '''
    Cria um cabeçalho UDP
    '''
    #transforma os valores em bytes usando o método to_bytes 
    porta_origem_bytes: bytes = porta_origem.to_bytes(length=2, byteorder="big")
    porta_destino_bytes: bytes = porta_destino.to_bytes(lenght=2, byteorder="big")
    comprimento_bytes: bytes = lenght.to_bytes(lenght=2, byteorder="big")
    checksum_bytes: bytes = checksum.to_bytes(lenght=2, byteorder="big")

    #retorna o cabeçalho UDP concatenando os bytes
    return porta_origem_bytes + porta_destino_bytes + comprimento_bytes + checksum_bytes + payload

def cliente_raw(ip_servidor, porta_servidor):
    #socket do cliente UDP RAW
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    print ("\n* VOCÊ ESTÁ DENTRO DO CLIENTE RAW *")

    while True:
        print("\n SEJA BEM VINDO! SELECIONE UMA OPÇÃO: ")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. SAIR")

        escolha = input("Digite sua escolha (1-4): ")

        if escolha == "1":
            #dados e hora
            tipo_requisicao = 0
        elif escolha == "2":
            #mensagem motivacional
            tipo_requisicao = 1
        elif escolha == "3":
            #respostas emitidas pelo servidor
            tipo_requisicao == 2
        elif escolha == "4":
            #sair
            print("Saindo...")
            break
        else:
            print("Escolha inválida. Tente novamente.")
            continue
        
        #constroi cabeçalho UDP
        porta_origem = random.randint(1, 59155) #escolhe aleatoriamente uma porta de origem
        porta_destino = porta_servidor
        comprimento = 8 + len(str(tipo_requisicao)) #tamanho do cabeçalho UDP
        pseudo_cabecalho = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00" + struct.pack("!H", comprimento)
        payload = str(tipo_requisicao).encode("utf-8") #converte o tipo de requisição para bytes
        cabecalho_udp = create_udp_header(porta_origem, porta_destino, comprimento, 0, payload)
        checksum = calcular_checksum(pseudo_cabecalho, cabecalho_udp, payload)
        
        #envia o pacote UDP
        socket_cliente.sendto(cabecalho_udp + payload, (ip_servidor, porta_servidor))
        
        #recebe a resposta
        resposta, _ = socket_cliente.recvfrom(256)
        
        #analisa a resposta
        tipo_resposta, identificador, texto_resposta = analisar_resposta(resposta)
        print(f"\nRESPOSTA RECEBIDA: \nTIPO {tipo_resposta} \nID {identificador} \n{texto_resposta}")
        
    #fechando o socket
    socket_cliente.close()
    
def main():
    #informações do servidor
    ip_servidor = "15.228.191.109"
    porta_servidor = 5000
    
    cliente_raw(ip_servidor, porta_servidor)
    
if __name__ == "__main__":
    main()
