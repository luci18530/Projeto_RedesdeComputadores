from sockets.udp import cliente_udp
from sockets.raw import cliente_raw

"""
GRUPO: ISABELLA NUNES DE OLIVEIRA, 
LUCIANO PEREIRA DE OLIVEIRA FILHO E
PEDRO LUCAS DA SILVA DOS SANTOS
"""

"""
O ÚNICO ARQUIVO QUE DEVE SER EXECUTADO É ESSE.
"python main.py"
"""


def main():
    # informações do servidor
    ip_servidor = "15.228.191.109"
    porta_servidor = 50000

    while True:
        print("\n* Bem-vindo ao sistema de requisições UDP/RAW *")
        print("\nSelecione uma opção:")
        print("1. Requisição UDP Socket")
        print("2. Requisição RAW Socket")
        print("3. Sair")

        escolha = input("Digite sua escolha (1-4): ")

        if escolha == "1":
            cliente_udp(ip_servidor, porta_servidor)
        elif escolha == "2":
            cliente_raw(ip_servidor, porta_servidor)
        elif escolha == "3":
            print("\nSaindo do programa principal...")
            break
        else:
            print("Escolha inválida")


if __name__ == "__main__":
    main()
