import json
import socket
import threading

"""
Ack(server_address): envia uma mensagem ACK para um ponto em uma rede ponto a ponto.
O metodo utiliza um único argumento, server_address, que especifica o endereço e a porta do servidor para o qual a mensagem ACK será enviada.
O metodo primeiro cria um socket UDP e dá bind ao endereço e porta do servidor especificados.
De seguida, entra num loop, à espera de receber mensagens dos nodos. Quando uma mensagem é recebida, a função verifica se o par já foi reconhecido.
Caso contrário, o metodo constrói uma mensagem ACK com parâmetros adicionais, codifica a mensagem como uma string JSON e a envia para o nodo seguinte.
O metodo por fim adiciona o nodo à lista de acknowledged_peers, para evitar o envio de várias mensagens ACK para o mesmo nodo (double flooding).
"""


def ack(server_address):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Keep track of which peers we have already acknowledged
    acknowledged_peers = []

    while True:
        # Receive message from peer
        print('Waiting to receive')
        data, peer_address = sock.recvfrom(4096)

        # Check if we have already acknowledged this peer
        if peer_address not in acknowledged_peers:
            # Create ACK message with additional parameters
            ack_message = {
                'message': 'ACK',
                'hops': 1,  # Number of hops from this peer to the destination
                'time_between_hops': 0.5,  # Time in seconds between hops
                'fast_path': True,  # Indicates if this is the fastest path from the peer to the destination
            }

            # Encode ACK message as JSON string
            ack_message_json = json.dumps(ack_message)

            # Send ACK message
            print('Sending ACK to {} port {}'.format(*peer_address))
            sock.sendto(ack_message_json.encode(), peer_address)

            # Add peer to acknowledged list
            acknowledged_peers.append(peer_address)


"""
Filter_Ack(server_address): 
O nodo escuta as mensagens recebidas e verifica o conteúdo da mensagem recebida.
Se a mensagem for uma mensagem ACK, ela será tratada separadamente das mensagens normais.
Isso permite que o nodo filtre e processe mensagens ACK numa Thread separada, atualizando a tabela de informações sem afetar o desempenho da aplicação.
"""


def filter_ack(server_address):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the specified server address
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    while True:
        # Receive message from peer
        print('Waiting to receive')
        data, peer_address = sock.recvfrom(4096)

        # Check if message is an ACK message
        if data == b'ACK':
            # Handle ACK message in a separate thread
            ack_thread = threading.Thread(target=handle_ack, args=(peer_address,))
            ack_thread.start()
        else:
            # Handle regular message
            handle_message(data)


def handle_ack(peer_address):
    # Update table of information with peer address and ACK information
    print('Received ACK from {} port {}'.format(*peer_address))
    # Call the ack function to send an ACK message to the peer
    ack(peer_address)


def handle_message(data):
    # Process regular message
    print('Received message {!r}'.format(data))
