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
            'Version': 'HTTP/1.1',
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

        # Making sure the request is at least HTTP
        req_base_mtch = re.match(r'(\w*) (.*) (.*)', req_base)
        if not req_base_mtch:
            print('Invalid request')
            self.res['Status'] = '400 Bad Request'
            return self.res
        
        self.req['Type'] = req_base_mtch.group(1)
        self.req['Path'] = req_base_mtch.group(2)

        # parse remaining request headers, assumes no body
        for param in req_split[1:]:
            key = param.split(':')[0].strip()
            val = param.split(':')[1].strip()
            self.req['Headers'][key] = val

        if self.req['Type'] == 'GET':
            if self.req['Path'] == '/' or self.req['Path'] == '/favicon.ico':
                self.req['Path'] = '/index.html'
            
            if self.req['Path'].endswith('.jpg'):
                self.res['Headers']['Content-Type'] = 'image/jpeg'
            elif self.req['Path'].endswith('.gif'):
                self.res['Headers']['Content-Type'] = 'image/gif'   
            elif self.req['Path'].endswith('.png'):
                self.res['Headers']['Content-Type'] = 'image/png'                                        
            elif self.req['Path'].endswith('.html'):
                self.res['Headers']['Content-Type'] = 'text/html'
            elif self.req['Path'].endswith('.mp3'):
                self.res['Headers']['Content-Type'] = 'audio/mp3'    
            elif self.req['Path'].endswith('.txt'):
                self.res['Headers']['Content-Type'] = 'text/plain' 
            else: 
                print('Unsupported document type')
                self.res['Status'] = '400 Bad Request'
                return self.res
            
            try:                                              
                f = open(self.res['Path'][1:], 'rb')
            except:
                print('Requested file not found')
                self.res['Status'] = '400 Bad Request'
                return self.res
            else:
                self.res['Body'] = f.read()

        elif self.req['Type'] == 'POST':
            # We would normally handle POST reqs here but the client is only requesting info here.
            return self.res
        else:
            print('Invalid request type')
            self.res['Status'] = '400 Bad Request'
            return self.res

        return self.res


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
                print('ress queue empty - nothing to send')
            else: # executes if no exception is caught
                to_send = bytearray(f'{res["Version"]} {res["Status"]}\r\n'.encode())
                for header, value in res['Headers'].items():
                    to_send.extend(f'{header}: {value}\r\n'.encode())
                to_send.extend('\n')
                to_send.extend(bytearray(res['Body']))
                s.send(to_send)
                print(f'HTTP res sent: \n{to_send.decode()}')

        for s in exceptional:
            socks.remove(s)
            s.close()
            del ress[s]
except:
    server.close()