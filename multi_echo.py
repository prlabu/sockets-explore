import select, socket, sys, queue, re
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 8080))
server.listen(5)
print(f'Server listening at port: 8080')
socks = [server]
reqs = {}
ress = {}

class HTTPReq:

    def __init__(self, raw_req):
        self.raw_req = raw_req.decode()
        self.res = {
            'Version': '',
            'Status': '',
            'Headers': {
                'Content-Type': ''
            }, 
            'Body': ''
        }
        self.req = {
            'Type': '',
            'Version': '',
            'Path': '',
            'Headers': {
                'Content-Type': ''
            }, 
            'Body': ''
        }

    def get_response(self):
        req_split = re.split(r'\r\n', (self.raw_req))
        req_base = req_split[0]

        # Making sure the request is valid at all 
        req_base_mtch = re.match(r'(\w*) (.*) (.*)', req_base)
        if not req_base_mtch:
            print('Invalid request')
            self.res
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
                return to_send

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


try: 
    while socks:
        readable, writable, exceptional = select.select(
            socks, socks, socks)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print(f'New TCP connection from: {client_address}')
                connection.setblocking(0)
                socks.append(connection)
                ress[connection] = queue.Queue()
            else:
                data = s.recv(1024).decode()
                if data:
                    print(f'Message recv: {data}')
                    reqObj = HTTPReq(data)
                    res = reqObj.get_response() # this will be a response dictionary
                    ress[s].put(data)
                else:
                    socks.remove(s)
                    s.close()
                    del ress[s]

        for s in writable:
            try:
                res = ress[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else: # executes if no exception is caught
                to_send = 
                s.send(next_msg)
                print(f'Message sent: {next_msg}')

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
except:
    server.close()