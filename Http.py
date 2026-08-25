class Http:
    http_version = "HTTP/1.1"
    def __init__(self):
        self.head = {}
        self.body = b""
        self.star_line = ""

        self.head_completed = False
        self.body_completed = False

    def add_header(self,name_header:str,content_header:str):
        self.head[name_header] = content_header

    def remove_header(self,name_header:str):
        if name_header in self.head:
            self.head.pop(name_header)

    def header_to_string(self,name_header:str):
        return f"{name_header}: {self.head[name_header]}\r\n"

    def update_content_lenth(self):
        if not "Content-Length" in self.head and len(self.body) == 0:
            return

        self.add_header("Content-Length",str(len(self.body)))

    def set_body(self,new_body:bytes):
        self.body = new_body
        self.update_content_lenth()

    def parse_HTTP_message(self,http_message:bytes):
        self.body += http_message
        if not self.head_completed:
            print("Parseando Head")
            if b"\r\n\r\n" in self.body:
                print("Head Completado")
                self.head_completed = True
                message_splited = self.body.split(b"\r\n\r\n")
                head_aux = message_splited[0].decode().split("\r\n")
                self.body = b""
                if len(message_splited) > 1:
                    self.body = message_splited[1]
                self.star_line = head_aux[0]
                for header in head_aux[1:]:
                    header_splited = header.split(": ")
                    self.head[header_splited[0]] = header_splited[1]
                else:
                    return
        if not self.body_completed:
            print("Parseando Body")
            final_length = 0
            if "Content-Length" in self.head:
                final_length = int(self.head["Content-Length"])
            current_length = len(self.body)
            if current_length >= final_length:
                print("Body Completado")
                self.body_completed = True
                self.update_content_lenth()

    def head_to_string(self):
        message = self.star_line + "\r\n"
        for header in self.head:
            message += header + ": " + self.head[header] + "\r\n"
        message += "\r\n"
        return message

    def create_String(self):
        return self.head_to_string() + self.body.decode()

    def create_HTTP_message(self):
        return self.head_to_string().encode() + self.body

    def create_REQUEST(self,type,root=""):
        self.star_line = f"{type} /{root} {self.http_version}"

    def create_RESPONSE(self,ncode,scode):
        self.star_line = f"{self.http_version} {ncode} {scode}"

    def create_HTML(self,html,parameter=None):
        cont = "text/html"
        if parameter != None:
            cont += f"; charset={parameter}"
        self.add_header("Content-Type",cont)
        self.set_body(html.encode())


