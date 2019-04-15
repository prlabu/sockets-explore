import socket
import logging
import requests as reqs
from requests import Request
import select
import queue

# logging.basicConfig(level=logging.DEBUG)

req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
req2 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
req3 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"

reqs = queue.Queue() 
reqs.put(req1)
reqs.put(req2)
reqs.put(req3)
ress = 0
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli.connect(('localhost', 8080))

while True:
    readable, writeable, exceptions = select.select([cli], [cli], [cli], 1)
    if cli in readable:
        msg_len = int.from_bytes(cli.recv(4), byteorder='big')
        res = cli.recv(msg_len).decode()
        if not res:
            print('Nothing to recv from client, breaking')
            break
        print(f'Obj recv: {res}\n')
        ress += 1
        # if ress >= 2:
        #     print('Responses received: breaking')
        #     break
    if cli in writeable:
        if not reqs.empty():
            req = reqs.get()
            req_bytes = req.encode()
            req_len = len(req_bytes)
            cli.send(req_len.to_bytes(4, byteorder='big'))
            cli.sendall(req.encode())
            print(f'Req sent: \n{req}\n')
    if cli in exceptions:
        print('Exception: breaking')
        break
cli.close()




# req = Request('GET',  'http://localhost:8080', data='asdfdsfd', headers={'Connection': 'close'})


# cli = reqs.Session()
# res = cli.get('http://localhost:8080')
# res1 = cli.get('http://localhost:8080/plainText.txt')
# cli.close()
# print(res)
# print(res1)


# res = reqs.get('http://localhost:8080')
# res1 = reqs.get('http://localhost:8080')
# print(res)
# print(res1)
