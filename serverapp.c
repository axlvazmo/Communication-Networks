#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include "comp.h"

int main(int argc, char** argv){
    
    /* Validating input from CLI*/
    if(argc < 12){
        printf("Usage: clientapp servIPAddr transaction number1 number2 number3... number10\n");
        return 0;
    }

    /* initial definitions */
    int client_socket, connection_status;               // variables containing handles and status of client socket
    char server_IP[20];                                 // contains the IP address of server
    unsigned int port_number = TCP_PORT;                // port number of server, 5000 used in this case
    struct sockaddr_in client;                          // client structure

    strcpy(server_IP, argv[1]);                         // pre-processing IP addr from CLI 

    /* server structure setup */
    client.sin_family = AF_INET;
    client.sin_addr.s_addr = inet_addr(server_IP);
    client.sin_port = htons(port_number);

    /* setting up structure to send to server */
    sBank_PROTOCOL client_request;                      // data structure for opperation type and opperands
    for(int i = 3; i < 13; i++){
        client_request.numbers[i-3] = atoi(argv[i]);    // processing opperands from the CLI to the data struct
    }
    client_request.opperation = atoi(argv[2]);          // processing opperation selection to the data struct

    /* Creating Socket */
    client_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);      // creating client socket
    if(client_socket < 0){
        printf("Error: socket not created\n");                      // if socket() returns -1, echo error
        return -1;
    }else{printf("Socket Created Successbully\n");}                 // otherwise echo success

    /* Connecting to server */
    connection_status = connect(client_socket, (struct sockaddr *) &client, sizeof(client));    // connect socket to server
    if(connection_status < 0){
        printf("Error: Connection unsuccessful\n");                                             // if connect() returns -1, echo error
        return -1;
    }else{printf("Connection successful\n");}                                                   // otherwise echo success

    // /* Sending data to server */
    send(client_socket, &client_request, sizeof(client_request), 0);                            // send data structure to server
    printf("Waiting for answer from server\n");

    /* Receiving data from server */
    double server_answer;                                       // buffer for server response
    recv(client_socket, &server_answer, sizeof(double), 0);     // capturing server answer
    printf("Feedback from server: %f\n", server_answer);        // echo server answer, contains result of opperation
    close(client_socket);                                       // closing socket
}