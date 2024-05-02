from udp import cliente_udp
from raw import cliente_raw


def main():
    # Informações do servidor
    ip_servidor = "15.228.191.109"
    porta_servidor = 50000

    while True:
        print("\n* Bem-vindo ao sistema de requisições UDP/RAW *")
        print("\nSelecione uma opção:")
        print("1. Requisição UDP Socket")
        print("2. Requisição RAW Socket (A FAZER)")
        print("3. Sair")

        escolha = input("Digite sua escolha (1-4): ")

        if escolha == "1":
            cliente_udp(ip_servidor, porta_servidor)
        elif escolha == "2":
            cliente_raw(ip_servidor, porta_servidor)  ## a ser implementado
        elif escolha == "3":
            print("\nSaindo do programa principal...")
            break
        else:
            print("Escolha inválida")


if __name__ == "__main__":
    main()
