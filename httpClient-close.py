import select, socket, sys, queue, time, argparse


def make_client_keepAlive_requests(num_iters):

    req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: close"
    req2 = "GET /flat.jpg HTTP/1.1\r\nConnection: close"
    req3 = "GET /food.mp3 HTTP/1.1\r\nConnection: close"

    reqs = queue.Queue() 

    # for iter in range(NUM_REQS_TO_SEND):
    #     reqs.put(req1)

    for _ in range(num_iters):
        reqs.put(req1)
        reqs.put(req2)
        reqs.put(req3)

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

    timed = 1000*(time.time() - start)
    return num_reqs, timed







if __name__ == "__main__":
    # number of iterations to request the three .jpg, .mp3, .txt files
    num_iters = 1 
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        num_iters = int(sys.argv[1])
    else:
        raise Exception('Incorrect command line usage. Use "python filename.py [num_iterations]"')

    num_requests, total_time = make_client_keepAlive_requests(num_iters)

    print('\nTotal of ({}) connection:close requests and responses completed in ({:.2f} ms).\n'.format(num_requests, total_time))
    
    # used for experimentation
    # outstr = f'{num_requests},{num_requests}\n'
    # with open('close.csv', 'a') as f: 
    #     f.write(outstr)







