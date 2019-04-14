// select() is used to handle multiple connections at one time 



int main(int argc, char const *argv[])
{
    /* code */
    return 0;

    int fd, next = 0, connfd, sockfd;
    int readfd[10];
    fd_set readfds, allfds;
    fd = socket();
    bind();
    listen();

    FD_ZERO(& allfds); // this will contains ALL sockets that are currently open, and initializes to zero. 
    FD_SET(fd, & allfds); // there is only one socket 


    while(1)
    {
        readfds = allfds; // this is such that, when we pass the array to select() the array isn't zeroed out
        select(maxfd + 1, & readfds, 0, 0); // select returns when at least one socket is ready
        if(FD_ISSET(fd, &readfds)) // if this is true, then a new socket is ready ! and we want to handle
        {
            connfd = accept(fd, ...)
            new[next] = connfd;
            next += 1; 
            FD_SET(connfd, &allfds);
        }

        for (all entries in new[]) 
        {
            sockfd = new[i];
            if (FD_SET(sockfd, &readfds))
            {
                handle new connection    
            }
        }
    }

    // in general, there is just one socket that is always listening... then there are others that are opened
    // for sending and rcving data. 
}
