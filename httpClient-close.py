import socket
import logging

# logging.basicConfig(level=logging.DEBUG)

req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: close"
req2 = "GET /flat.jpg HTTP/1.1\r\nConnection: close"
req3 = "GET /food.mp3 HTTP/1.1\r\nConnection: close"
reqs = [req1, req2, req3]

for req in reqs:
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect(('localhost', 8080))
    cli.sendall(req.encode())
    print(f'Req sent: \n{req}\n')
    res = cli.recv(1024)
    print(f'Obj recv\n')
    cli.close()










