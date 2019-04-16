import select, socket, sys, queue, time

def make_client_close_requests(num_iters):

    req1 = "GET /plainText.txt HTTP/1.1\r\nConnection: keep-alive"
    req2 = "GET /food.mp3 HTTP/1.1\r\nConnection: keep-alive"
    req3 = "GET /flat.jpg HTTP/1.1\r\nConnection: keep-alive"

    reqs = queue.Queue() 

    for i in range(num_iters):
        reqs.put(req1)
        reqs.put(req2)
        reqs.put(req3)

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
                # print('Nothing to recv from client, breaking')
                break
            # print(f'Obj recv: \n')
            num_ress += 1

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

    num_requests, total_time = make_client_close_requests(num_iters)

    print('\nTotal of ({}) keep-alive requests and responses completed in ({:.2f} ms).\n'.format(num_requests, total_time))
    outstr = f'{num_requests},{num_requests}\n'
    with open('keep-alive.csv', 'a') as f: 
        f.write(outstr)





