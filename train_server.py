import socket
import select


server_ip = '25.82.159.185'
server_port = 5060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)


server_launched = True
clients_active = []
while server_launched:
    asked_connections, wlist, xlist = select.select([server], [], [], 0.05)

    for connection in asked_connections:
        client_online, client_info = connection.accept()
        clients_active.append(client_online)
        client_online.send(b"Vous etes connecte sur le serveur")

    client_to_read = []
    try:
        client_to_read, wlist, xlist = select.select(clients_active, [], [], 0.05)
    except select.error:
        pass
    else:
        for client in client_to_read:
            received_msg = client.recv(1024)
            received_msg = received_msg.decode()
            print clients_active
            print(received_msg)
            client.send(b"5/5")

            if received_msg == "fin":
                server_launched = False

for client in clients_active:
    client.close()
server.close()
