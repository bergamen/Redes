import socket
import json
import sys
from Http import Http

IP_VM = '192.168.100.116'
PUERTO_VM = 8000

def http_parse(socket_listen,buf_size):
    http_aux = Http()
    while not http_aux.body_completed:
        try:
            recv = socket_listen.recv(buf_size)
        except:
            raise
        if not recv:
            raise
        http_aux.parse_HTTP_message(recv)
    return http_aux

def read_all_file(file,par = None):
    if par == None:
        file_opened = open(file)
    else:
        file_opened = open(file,par)
    text = file_opened.read()
    file_opened.close()
    return text

if __name__ == "__main__":
    buff_size = 1024
    new_socket_address = (IP_VM,PUERTO_VM)

    with open(f"{sys.argv[1]}/{sys.argv[2]}.json") as file:
        data = json.load(file)
        usuario = data["user"]
        prohibidos = data["blocked"]
        censura = data["forbidden_words"]  

    print('Creando socket - Proxy')

    cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    cliente_socket.bind(new_socket_address)


    cliente_socket.listen(3)
    print('... Esperando clientes')

    while True:
        new_socket,new_socket_address = cliente_socket.accept()
        new_socket.settimeout(1)
        http_recv = http_parse(new_socket,buff_size)
        IP_HOST = http_recv.head["Host"]
        print(IP_HOST)
        sitio = http_recv.star_line.split(" ")[1].replace("http://","")
        if not sitio in prohibidos:

            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_socket.settimeout(1)
            address_server = (IP_HOST,80)
            try:
                server_socket.connect(address_server)
            except:
                new_socket.close()
                break

            while True:
                print("Entrando al ciclo")
                print(http_recv.create_String())
                http_recv.add_header("X-ElQuePregunta",usuario)
                server_socket.send(http_recv.create_HTTP_message())
                try:
                    http_response = http_parse(server_socket,buff_size)
                except:
                    break
                http_response.censurar(censura)
                print(http_response.create_String())
                new_socket.send(http_response.create_HTTP_message())
                try:
                    http_recv = http_parse(new_socket,buff_size)
                except:
                    break
                

            server_socket.close()
        else:
            print("Sitio prohibido")
            http_response = Http()
            http_response.create_RESPONSE(200,"OK")
            http_response.add_header("X-ElQuePregunta",usuario)
            http_response.add_header("Connection","keep-alive")
            http_response.create_HTML(read_all_file("html/error.html"),"UTF-8")
            print(http_response.create_String())
            new_socket.send(http_response.create_HTTP_message())
            print("Buscando Gatito")
            try:
                http_image = http_parse(new_socket,buff_size)
                print("Gatito Recibido")
                print(http_image.create_String())

                dir = http_image.star_line.split(IP_HOST)[1][1:].split(" ")[0]
                http_response_image = Http()

                http_response_image.create_RESPONSE(200,"OK")
                http_response_image.add_header("X-ElQuePregunta",usuario)
                http_response_image.create_IMAGE(read_all_file(dir,"rb"))
                new_socket.send(http_response_image.create_HTTP_message())
            except:
                pass
        
        new_socket.close()
        print(f"conexión con {new_socket_address} ha sido cerrada")

