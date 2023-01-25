#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include "comp.h"


int main(){
    int server_socket, connection_status;                           // variables containing handles and status of server socket
    int bind_status, listen_status;                                 // variables containing handles and status of server socket
    double sum, mean, min, max;                                     // variables that contain the result of opperations
    unsigned int port_number = TCP_PORT;                            // port number of server, 5000 used in this case
    struct sockaddr_in server, client;                              // client and server structure

    /* Server structure setup */
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);                     // set to accept connection from any IP addr
    server.sin_port = htons(port_number);

    /* creating the socket */
    server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);      // creating server socket
    if(server_socket < 0){
        printf("Error: socket not created\n");                      // if socket() returns -1, echo error
        return -1;
    }else{printf("Socket Created Successfully\n");}                 // otherwise echo success

    /* Binding socket */
    bind_status = bind(server_socket, (struct sockaddr*) &server, sizeof(server));      // binding to server socket
    if(bind_status < 0){
        printf("Error: Could not bind to socket\n");                // if bind() returns -1, echo error
        return -1;
    }else{printf("Socket Bind Successfull\n");}                     // otherwise echo success

    /* Listening on the socket */
    listen_status = listen(server_socket, 5);                       // listening for client connection requests
    if(listen_status < 0){
        printf("Error: Socket Listen Failed\n");                    // if listen() returns -1, echo error
        return -1;
    }else{printf("Listening...\n");}                                // otherwise echo success

    /* Accepting connection */
    int len = sizeof(server);                                       // contains size of the server structure
    connection_status = accept(server_socket, (struct sockaddr *) &client, &len);   // accepting connection request from client
    if(connection_status < 0){
        printf("Error: Connection Unsuccessful\n");                 // if accept() returns -1, echo error
        return -1;
    }else{printf("Connection Successful\n");}                       // otherwise echo success

    /*Receiving data from client */
    sBank_PROTOCOL client_request;                                  // data structure with opperation choice and opperands
    recv(connection_status, &client_request, sizeof(client_request), 0);    // capturing client request data
    if(client_request.opperation == OP_SUM){
        sum = 0.0;
        for (int i = 0; i < 10; i++){
            sum = sum + client_request.numbers[i];                  // if opperation chosen is sum, summ all itmens in the array
        }
        send(connection_status, &sum, sizeof(double), 0);           // send back the result to server
    }else if(client_request.opperation == OP_MEAN){
        mean = 0.0;
        for (int i = 0; i < 10; i++){
            mean = mean + client_request.numbers[i];                // if opperation chosen is mean, summ all itmens in the array
        }
        mean = mean/(sizeof(client_request.numbers)/sizeof(double));    // divide by the # of elements in the array
        send(connection_status, &mean, sizeof(double), 0);          // send back the result to server
    }else if(client_request.opperation == OP_MIN){
        min = client_request.numbers[0];
            for (int i = 1; i < 10; i++){
                if (min > client_request.numbers[i]){               // if opperation chosen is min, iterate through the elements and find the smallest value
                    min = client_request.numbers[i];
                }
            }
            send(connection_status, &min, sizeof(double), 0);       // send back the result to server
    }else if(client_request.opperation == OP_MAX){
        max = client_request.numbers[0];
        for (int i = 0; i < 10; i++){
            if (max < client_request.numbers[i]){                   // if opperation chosen is max, iterate through the elements and find the largest value
                max = client_request.numbers[i];
            } 
        }
        send(connection_status, &max, sizeof(double), 0);           // send back the result to server
    }
    close(connection_status);                                       // closing the connection with client
    close(server_socket);                                           // closing the socket
}