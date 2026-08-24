import socket
from Http import Http

IP_VM = '192.168.100.114'
IP_SR = '0.0.0.0' 

def read_HTML(file):
    html = open(file+".html")
    text = html.read()
    html.close()
    return text

if __name__ == "__main__":
    buff_size = 4
    end_of_message = "\n"
    new_socket_address = (IP_VM,8000)

    print('Creando socket - Servidor')

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_socket.bind(new_socket_address)

    server_socket.listen(3)
    print('... Esperando clientes')

    while True:
        new_socket,new_socket_address = server_socket.accept()
        http_recv = Http()
        while not http_recv.body_completed:
            http_recv.parse_HTTP_message(new_socket.recv(buff_size))
        print(http_recv.create_String())

        http_response = Http()
        http_response.create_RESPONSE(200,"OK")
        http_response.add_header("X-ElQuePregunta","VicenteBenja")
        http_response.create_HTML(read_HTML("test"),"UTF-8")
        print("Respuesta:\n"+http_response.create_String())
        new_socket.send(http_response.create_HTTP_message())
        new_socket.close()
        print(f"conexión con {new_socket_address} ha sido cerrada")
