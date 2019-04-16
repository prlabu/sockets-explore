import socket
import logging
import time
import queue
import sys 


if __name__ == "__main__":
    NUM_REQS_TO_SEND = int(sys.argv[1])

    req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: close"
    req2 = "GET /flat.jpg HTTP/1.1\r\nConnection: close"
    req3 = "GET /food.mp3 HTTP/1.1\r\nConnection: close"

    reqs = queue.Queue() 


    for iter in range(NUM_REQS_TO_SEND):
        reqs.put(req1)

    # for i in range(15):
    #     reqs.put(req1)
    #     reqs.put(req2)
    #     reqs.put(req3)

    num_reqs = 0
    num_ress = 0

    start = time.time()

    while not reqs.empty():
        req = reqs.get()
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.connect(('localhost', 8080))
        
        req_len = len(req.encode())
        cli.send(req_len.to_bytes(4, byteorder='big'))
        cli.sendall(req.encode())

        # print(f'Req sent: \n{req}')
        res = cli.recv(1024)
        # print(f'Obj recv\n')
        num_reqs += 1
        num_ress += 1

        cli.close()

    print(f'Total total req ({num_reqs}), total res ({num_ress})')
    outstr = f'{NUM_REQS_TO_SEND},{1000*(time.time() - start)}\n'
    print(outstr)
    with open('keep-close.csv', 'a') as f: 
        f.write(outstr)








