HTTP Server and Clients (one Persistent, one Non-persistent)
===

The server and clients are implemented in Python3. The only dependences for the server are shown below, all of which should not require installing any external modules. The imports are the same for the client with the exception of time().
```Python
import select, socket, sys, queue, re
```


To run the server (Unix), use 
```
$ python httpServer.py 
```
This should start serving on port 8080, which is printed in terminal. The server prints in terminal every time a new client connects, a new HTTP message is received, or a client connection is closed. 



To run the client, use  
```Bash
$ python httpClient-keepAlive.py 5
```
... where the call format is 
```Bash
$ python httpClient-keepAlive.py [number_iterations]
```
`number_iterations` is the number of times the three message types (.jpg, .mp3, .txt) are retrieved. 

The client should be run on the same host as the server as the server serves on 'localhost'. You should get the following printed  in the terminal if the client made the requests and receieved the responses correctly. 
```
Total of (15) keep-alive requests made in (3.62 ms).
```

