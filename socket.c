#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<sys/uio.h>
#include<errno.h>
#include<sys/ioctl.h>
#include<fcntl.h>
#include<sys/socket.h>
#include<netdb.h>
#include<netinet/in_systm.h>
#include<netinet/ip_icmp.h>
#include<netinet/udp.h>
#include<netinet/ip.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<arpa/nameser.h>
#include<resolv.h>
#include<net/if.h>
#include<strings.h>


#define PORT_NO 10000

void main()
{
    int sock, len, cli, sent; 
    struct sockaddr_in server, client;
    char msg[] = "Hello world";

    if((sock = socket(AF_INET, SOCK_STREAM, 0)) == 1) 
    {
        perror("socket");
        exit(1);
    }

    server.sin_family = AF_INET;
    server.sin_port = htons(PORT_NO);
    server.sin_addr.s_addr = INADDR_ANY;

    bzero(&server.sin_zero, 0);

    len = sizeof(struct sockaddr_in);

    if(bind(sock, (struct  sockaddr *) &server, len) == -1)
    {
        perror("bind");
        exit(1);
    }  

    if(listen(sock, 5) == -1)
    {
        perror("lsiten");
        exit(1);
    }  
    // printf("send %d bytes of data to client: %s \n", sent, int_ntoa(client.sin_addr)); 
    // printf("Server listening on port", int_ntoa(client.sin_addr)); 


    while(1)
    {
        // this is a new socket through which we communicate with the client
        // all reads and writes will be done through CLI
        if((cli = accept(sock, (struct sockaddr *) &client, &len)) == -1)
        {
            perror("accept");
            exit(1);
        }
        
        // counts how many bytes we send to the otherside 
        sent = send(cli, msg, strlen(msg), 0);

        //int_ntoa converts to human readable address
        printf("send %d bytes of data to client: %s \n", sent, int_ntoa(client.sin_addr)); 

        close(cli);


    }

}