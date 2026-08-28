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
            message += self.header_to_string(header)
        message += "\r\n"
        return message

    def create_String(self):
        if self.head_completed:
            return self.head_to_string() + self.body.decode()
        else:
            return self.body.decode()

    def create_HTTP_message(self):
        return self.head_to_string().encode() + self.body


    def create_REQUEST(self,type,root=""):
        self.body_completed = True
        self.head_completed = True
        self.star_line = f"{type} /{root} {self.http_version}"

    def create_RESPONSE(self,ncode,scode):
        self.body_completed = True
        self.head_completed = True
        self.star_line = f"{self.http_version} {ncode} {scode}"

    def create_HTML(self,html,parameter=None):
        cont = "text/html"
        if parameter != None:
            cont += f"; charset={parameter}"
        self.add_header("Content-Type",cont)
        self.set_body(html.encode())
    def create_IMAGE(self,image,parameter = None):
        cont = "image/jpg"
        if parameter != None:
            cont += f"; parameter={parameter}"
        self.add_header("Content-Type",cont)
        self.set_body(image)

    def is_close(self):
        if "Connection" in self.head:
            if self.head["Connection"] == "keep-alive":
                return False
            elif self.head["Connection" ] == "close":
                return True
            else:
                return False

    # def is_REQUEST(self):
    #     request = ["GET","POST"]
    #     type_req = self.star_line.split(" ",1)[0]
    #     if type_req in request:
    #         return True
    #     else:
    #         return False

    # def get_type_REQUEST(self):
    #     return self.star_line.split(" ",1)[0]

    # def create_HTTP_by_REQUEST(self):
    #     if not self.is_REQUEST:
    #         return None
    #     type_req = self.get_type_REQUEST()
    #     if type_req == "GET":
            

    #[{"proxy": "[REDACTED]"}, {"DCC": "[FORBIDDEN]"}, {"biblioteca": "[???]"}]
    def censurar(self,palabras_prohibidas):
        if self.body_completed:
            for palabra_dic in palabras_prohibidas:
                for palabra in palabra_dic:
                    while palabra.encode() in self.body:
                        self.body = self.body.replace(palabra.encode(),palabra_dic[palabra].encode())
        self.update_content_lenth()
                        

            

            
