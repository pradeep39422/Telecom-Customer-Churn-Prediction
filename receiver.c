#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <Sender IP> <Receiver Port>\n", argv[0]);
        return 1;
    }

    int sockfd;
    struct sockaddr_in receiver_addr, sender_addr;
    char buffer[BUFFER_SIZE];
    socklen_t addr_len = sizeof(sender_addr);

    // Create UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        return 1;
    }

    memset(&receiver_addr, 0, sizeof(receiver_addr));
    receiver_addr.sin_family = AF_INET;
    receiver_addr.sin_port = htons(atoi(argv[2]));
    receiver_addr.sin_addr.s_addr = INADDR_ANY;

    // Bind the socket with the receiver address
    if (bind(sockfd, (const struct sockaddr *)&receiver_addr, sizeof(receiver_addr)) < 0) {
        perror("Bind failed");
        close(sockfd);
        return 1;
    }

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);

        // Receive message from sender
        recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&sender_addr, &addr_len);
        printf("Receiver: %s", buffer);

        // If the received message is "exit", close the socket and exit
        if (strncmp(buffer, "exit", 4) == 0) {
            printf("Exiting...\n");
            break;
        }

        // Send the received message back to the sender (echo)
        sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *)&sender_addr, addr_len);
    }

    close(sockfd);
    return 0;
}

