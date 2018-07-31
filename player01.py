import socket


server_ip = '127.0.0.1'
server_port = 5060

player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player.connect((server_ip, server_port))

msg_recieved = player.recv(1024)
print msg_recieved

msg_to_send = b""
while msg_to_send != b"fin":
    msg_to_send = raw_input(">")
    msg_to_send = msg_to_send.encode()
    player.send(msg_to_send)
    recieved_msg = player.recv(1024)
    print(recieved_msg.decode())

player.close()
