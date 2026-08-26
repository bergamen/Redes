import socket
import json
import sys
from Http import Http

IP_VM = '192.168.100.115'

def read_all_file(file,par = None):
    if par == None:
        file_opened = open(file)
    else:
        file_opened = open(file,par)
    text = file_opened.read()
    file_opened.close()
    return text

if __name__ == "__main__":
    buff_size = 4
    end_of_message = "\n"
    new_socket_address = (IP_VM,8000)

    with open(f"{sys.argv[1]}/{sys.argv[2]}.json") as file:
        data = json.load(file)
        usuario = data["usuario"]
        prohibidos = data["prohibidos"]

    print('Creando socket - Proxy')

    cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    cliente_socket.bind(new_socket_address)

    # server_socket.bind(new_socket_address)

    cliente_socket.listen(3)
    print('... Esperando clientes')

    while True:
        new_socket,new_socket_address = cliente_socket.accept()
        http_recv = Http()
        while not http_recv.body_completed:
            http_recv.parse_HTTP_message(new_socket.recv(buff_size))
        print(http_recv.create_String())

        IP_HOST = http_recv.head['Host'].split(":")[0]
        print(IP_HOST)
        http_response = Http()
        if not IP_HOST in prohibidos:
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            address_server = (IP_HOST,80)
            server_socket.connect(address_server)
            server_socket.send(http_recv.create_HTTP_message())
            while not http_response.body_completed:
                http_response.parse_HTTP_message(server_socket.recv(buff_size))
            print(http_response.create_String())
            new_socket.send(http_response.create_HTTP_message())
        else:
            http_response.create_RESPONSE(403,"ERROR")
            http_response.add_header("X-ElQuePregunta",usuario)
            http_response.create_HTML(read_all_file("html/error.html"),"UTF-8")
            new_socket.send(http_response.create_HTTP_message())
            http_image = Http()
            while not http_image.body_completed:
                http_image.parse_HTTP_message(new_socket.recv(buff_size))
            print(http_image.create_String())

            dir = http_image.star_line.split(IP_HOST)[1][1:].split(" ")[0]
            http_response_image = Http()

            http_response_image.create_RESPONSE(200,"OK")
            http_response_image.add_header("X-ElQuePregunta",usuario)
            http_response_image.create_IMAGE(read_all_file(dir,"rb"))
            new_socket.send(http_response_image.create_HTTP_message())
        
        new_socket.close()
        print(f"conexión con {new_socket_address} ha sido cerrada")
