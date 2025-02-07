import os
import socket

class TCPServer:
    def __init__(self, host = "127.0.0.1", port = 6969):
        self.host = host
        self.port = port
        
    def start(self):
        #creating a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        socket_address = (self.host, self.port)
        #bind socket to an address
        s.bind(socket_address)
        
        #make socket to listen
        s.listen(5)
        
        while True:
            conn_socket , adrr = s.accept()
            
            data = conn_socket.recv(1024)
            
            conn_socket.sendall(self.handle_request(data))
            
            conn_socket.close()
            
    def handle_request(self, data):
        return data
            
class HTTPServer(TCPServer):
    
    headers = {
        "Sever": "Vatafu Darius",
        "Content-Type" : "text/html",
    }
    
    status_codes = {
        200:"OK",
        404:"Not Found",
        501:"Not implemented",
    }
    
    def handle_request(self, data):
        request = HTTPRequest(data)
        
        try:
            handler = getattr(self, 'handle_%s' % request.method.decode())
        except AttributeError:
            handler = self.HTTP_501_handler
        
        response = handler(request)
        
        return response
    
    def response_line(self,status_code):
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)
        return line.encode()
    
    def response_headers(self, extra_headers = None):
        headers_copy = self.headers.copy()
        if extra_headers:
            headers_copy.update(extra_headers)
            
        headers = ""
        
        for h in headers_copy:
            headers += "%s : %s \r\n" % (h, headers_copy[h])
            
        return headers.encode()    
    def HTTP_501_handler(self, request):
        request_line = self.response_line(status_code = 501)
        
        headers = self.response_headers()
        
        blank_line = b"\r\n"
        
        response_body = b"<h1>501 Not implemented\r\n</h1>"
        
        return b"".join([request_line, headers, blank_line, response_body])
        
    #handling the GET request
    def handle_GET(self, request):
        
        filename = request.uri.strip('/')
        
        if os.path.exists(filename):
            response_line = self.response_line(status_code = 200)
            
            headers = self.response_headers()
            
            with open(filename, "rb" )as f:
                response_body = f.read()
        else:
            response_line = self.response_line(status_code = 404)
            
            headers = self.response_headers()
            response_body = b"<h1>Not Found</h1>"
            
        blank_line = b"\r\n"
        
        return b"".join([response_line, headers,blank_line,  response_body])    
            
        
class HTTPRequest:
    def __init__(self,data):
        #request parameters
        self.method = None
        self.uri = None
        self.http_version = "1.1"
        
        #parsing the request data to the server
        return self.parse(data)
    
    def parse(self,data):
        lines = data.split(b"\r\n")
        
        request_line = lines[0]
        
        words = request_line.split(b" ")
        
        #this is the method from the request
        self.method = words[0]
        
        if len(words) > 1:
            #this is the uri form the request
            self.uri = words[1].decode()
            
        if len(words) > 2:
            #this is the http version from the request
            self.http_version = words[2]
                
if __name__ == "__main__":
    server = HTTPServer()
    server.start()
        
        