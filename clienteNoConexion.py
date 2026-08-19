import socket

dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
message, address = dgram_socket.recvfrom(bufsize)

dgram_socket.sendto(message, address)