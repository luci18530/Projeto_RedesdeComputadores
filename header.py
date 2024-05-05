def create_udp_header(porta_origem:int, porta_destino:int, length:int, checksum:int, payload:int) -> bytes:
    '''
        Cria um cabeçalho udp.
    '''
    
    # a função "to_bytes" transforma o número "porta_origem" em bytes, o primeiro parametro "length" representa a quantidade de bytes que serão utilizados pra representar o número, o segundo "byteorder" fala qual byte é significativo, se é o primeiro ou o ultimo
    porta_origem_bytes:bytes = porta_origem.to_bytes(length=2, byteorder="big")
    porta_destino_bytes:bytes = porta_destino.to_bytes(length=2, byteorder="big")
    comprimento_bytes:bytes = length.to_bytes(length=2, byteorder="big")
    checksum_bytes:bytes = checksum.to_bytes(length=2, byteorder="big")
    payload_bytes:bytes = payload.to_bytes(length=3, byteorder="big")

    return (porta_origem_bytes + porta_destino_bytes + comprimento_bytes + checksum_bytes + payload_bytes)


def main():
    print(create_udp_header(59155, 50000, 11, 0, 23777))

if __name__ == "__main__":
    main()
