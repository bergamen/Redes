import socket

print('Creando socket - cliente')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('localhost',5000)
client_socket.connect(address)

message = "Hola, Mensaje de prueba"
end_message = "\n"

send_message = (message + end_message).encode()

print(f"...Mandando un mensaje: {send_message.decode()}")
client_socket.send(send_message)
print("...Mensaje enviado")

buffer_size = 1024
message = client_socket.recv(buffer_size)

decoded_message = message.decode()
print(f'-> Respuesta del servidor: {decoded_message}')

client_socket.close()