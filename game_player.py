import socket


server_ip = '127.0.0.1'
server_port = 5060

player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player.connect((server_ip, server_port))


player_online = True
while player_online:
    msg_recieved = player.recv(1024)
    msg_to_show = msg_recieved[3:]
    print(msg_to_show)

    if "_w_" in msg_recieved:
        msg_to_send = raw_input(">")
        msg_to_send = msg_to_send.encode()
        player.send(msg_to_send)


player.close()