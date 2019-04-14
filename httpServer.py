from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import re
import os
from os import curdir, sep
from pprint import pprint
from time import time
import socket
import select

PORT_NUMBER = 8080


class HTTPRequestHandler(socketserver.BaseRequestHandler):
    # The connection is closed when handle() returns
    # This handle is for every new TCP connection (every new client), not for every new HTTP req
    # For persistent connections, we have to handle multiple HTTP reqs per TCP connection
    def handle(self):
        self.close_connection = False
        self.timeout_len = 0.2
        self.start_time = time()
        print(f'New TCP connection: {self.client_address}')

        # self.request.setblocking(0)

        while (not self.close_connection):
            print('place1')
            # ready = select.select([self.request], [], [], self.timeout_len)
            # if ready[0]:
            #     self.data = self.request.recv(1024).strip().decode('utf-8')
            # else:
            #     self.close_connection = True
            #     break

            self.data = self.request.recv(1024).strip().decode('utf-8')
            print(self.data)
            
            self._handleHTTPReq(self.data)
            
            # Connection timeout - client has made no requests
            # if time() - self.start_time > self.timeout_len:
            #     self.close_connection = True
        
        print(f'Closing TCP connection: {self.client_address} \n')

    def _handleHTTPReq(self, HTTPReq):
        self.http_res = {}

        req_split = re.split(r'\r\n', (self.data))
        req_base = req_split[0]

        req_base_mtch = re.match(r'(\w*) (.*) (.*)', req_base)
        if not req_base_mtch:
            print('Invalid request')
            return
        req_type = req_base_mtch.group(1)
        req_path = req_base_mtch.group(2)

        req_params = {}
        for param in req_split[1:]:
            key = param.split(':')[0].strip()
            val = param.split(':')[1].strip()
            req_params[key] = val

        print(f'New HTTPreq, Connection type: {req_params["Connection"]}')
        if req_params['Connection'] == 'keep-alive':
            self.close_connection = True
        else:
            self.close_connection = True

        if req_type == 'GET':
            if req_path == '/' or req_path == '/favicon.ico':
                req_path = '/index.html'
    
            try:
                if req_path.endswith('.jpg'):
                    self.http_res['Content-Type'] = 'image/jpeg'
                elif req_path.endswith('.gif'):
                    self.http_res['Content-Type'] = 'image/gif'   
                elif req_path.endswith('.png'):
                    self.http_res['Content-Type'] = 'image/png'                                        
                elif req_path.endswith('.html'):
                    self.http_res['Content-Type'] = 'text/html'
                elif req_path.endswith('.mp3'):
                    self.http_res['Content-Type'] = 'audio/mp3'    
                elif req_path.endswith('.txt'):
                    self.http_res['Content-Type'] = 'text/plain'                                               
                
                f = open(req_path[1:], 'rb')

                to_send = bytearray('HTTP/1.1 200 OK\r\n'.encode())
                to_send.extend(f'Content-Type: {self.http_res["Content-Type"]}\r\n'.encode())
                to_send.extend(b'\n')
                to_send.extend(bytearray(f.read()))
                self.request.sendall(to_send)

            except IOError:
                print(f'invalid path: {req_path}')
                to_send = bytearray('HTTP/1.1 404 FileNotFound\r\n'.encode())
                to_send.extend(b'\r\n\n')
                self.request.sendall(to_send)

        elif req_type == 'POST':
            # We would normally handle POST reqs here but the client is only requesting info here.
            return
        else:
            print('invalid request type')

        return

 
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    try: 
        # Create the server, binding to localhost on port 8080
        with socketserver.TCPServer((HOST, PORT), HTTPRequestHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print(f'Serving at IP ({server.server_address[0]}), Port ({server.server_address[1]})')
            server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.close()














# #This class will handles any incoming request from
# #the browser 
# class myHandler(BaseHTTPRequestHandler):
    
# 	#Handler for the GET requests
# 	def do_GET(self):
# 		self.send_response(200)
# 		# self.send_header('Content-type','text/html')
# 		self.send_header('Content-type','text/html')
# 		self.end_headers()
# 		# Send the html message
        
# 		with open('flat.jpg') as f:
# 			# self.wfile.write(f.read().encode())
# 			self.wfile.write("Hi world !".encode())
# 		return




# try:
# 	#Create a web server and define the handler to manage the
# 	#incoming request
# 	server = HTTPServer(('', PORT_NUMBER), myHandler)
# 	print('Started httpserver on port ' , PORT_NUMBER)
    
# 	#Wait forever for incoming htto requests
# 	server.serve_forever()

# except KeyboardInterrupt:
# 	print('^C received, shutting down the web server')
# 	server.socket.close()