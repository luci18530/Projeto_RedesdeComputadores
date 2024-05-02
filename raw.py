import random
import socket

def gerar_identificador():
    return random.randint(1, 65535)

def main():
     # Informações do servidor
    ip_servidor = "15.228.191.109"
    porta_servidor = 50000

    # Socket do cliente UDP RAW
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RDP)

    print("\nBem-vindo ao sistema de requisições UDP RAW!")

    while True:
        print("\nSelecione uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")

        escolha = input("Digite sua escolha (1-4): ")

if __name__ == "__main__":
    main()