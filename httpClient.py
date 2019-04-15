import socket
import logging

# logging.basicConfig(level=logging.DEBUG)

req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
req2 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
req3 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"

reqs = [req1, req2, req3]
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli.connect(('localhost', 8080))

for req in reqs:
    
    cli.sendall(req.encode())
    print(f'Req sent: \n{req}\n')
    res = cli.recv(1024).decode()
    print(f'Obj recv: {res}\n')

cli.close()
