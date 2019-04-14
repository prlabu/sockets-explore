
int main(int argc, char const *argv[])
{
    int fd; 
    struct sock_addr_in;

    fd = socket()
    bind(fd, ...);
    listen(fd, ...);

    while(1)
    {
        connfd = accept(fd, ...); // when accept returns, we have a connection

        pid = fork(); // process id that we will use to determine whether child or parent
        if(pid == 0) // means we are a child
        {
            close(fd); // the new connections are the responsibility of the parent

            // then handle connection with things like rcv() and send(), then close(connfd);
            recv();
            setid();
            close(connfd);
            exit(0); // exit successfully
        }

        close(connfd); // this executes if we are the parent
        
        

    }
}
