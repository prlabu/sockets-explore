import socket
import logging
import requests as reqs
from requests import Request
import select
import queue
import time
import sys

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    NUM_REQS_TO_SEND = int(sys.argv[1])

    req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
    req2 = "GET /food.mp3 HTTP/1.1\r\nConnection: keep-alive"
    req3 = "GET /flat.jpg HTTP/1.1\r\nConnection: keep-alive"

    reqs = queue.Queue() 

    for iter in range(NUM_REQS_TO_SEND):
        reqs.put(req1)

    # for i in range(15):
    #     reqs.put(req1)
    #     reqs.put(req2)
    #     reqs.put(req3)
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    num_reqs = 0
    num_ress = 0


    start = time.time()

    cli.connect(('localhost', 8080))

    while True:
        readable, writeable, exceptions = select.select([cli], [cli], [cli], 1)
        if cli in readable:
            msg_len = int.from_bytes(cli.recv(4), byteorder='big')
            res = cli.recv(msg_len)
            if not res:
                print('Nothing to recv from client, breaking')
                break
            # print(f'Obj recv: \n')
            num_ress += 1
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
                # print(f'Req sent: \n{req}\n')
                num_reqs += 1
        if cli in exceptions:
            print('Exception: breaking')
            break
    cli.close()
    print(f'Total total req ({num_reqs}), total res ({num_ress})')
    outstr = f'{NUM_REQS_TO_SEND},{1000*(time.time() - start)}\n'
    print(outstr)
    with open('keep-alive.csv', 'a') as f: 
        f.write(outstr)



