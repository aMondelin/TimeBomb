import socket


server_ip = "25.82.159.185"
server_port = 5060

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

msg = client.recv(1024)
print msg

msg_to_send = b""
while msg_to_send != b"fin":
    msg_to_send = raw_input(">")
    msg_to_send = msg_to_send.encode()
    client.send(msg_to_send)
    recieved_msg = client.recv(1024)
    print(recieved_msg.decode())

client.close()
