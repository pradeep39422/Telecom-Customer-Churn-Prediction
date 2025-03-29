#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <Receiver IP> <Receiver Port>\n", argv[0]);
        return 1;
    }

    int sockfd;
    struct sockaddr_in receiver_addr;
    char buffer[BUFFER_SIZE];
    
    // Create UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        return 1;
    }

    memset(&receiver_addr, 0, sizeof(receiver_addr));
    receiver_addr.sin_family = AF_INET;
    receiver_addr.sin_port = htons(atoi(argv[2]));
    receiver_addr.sin_addr.s_addr = inet_addr(argv[1]);

    while (1) {
        printf("Sender: ");
        fgets(buffer, BUFFER_SIZE, stdin);

        // Send message to receiver
        sendto(sockfd, buffer, strlen(buffer), 0, (const struct sockaddr *)&receiver_addr, sizeof(receiver_addr));

        // If the message is "exit", close the socket and exit
        if (strncmp(buffer, "exit", 4 == 0)) {
            printf("Exiting...\n");
            break;
        }
    }

    close(sockfd);
    return 0;
}

