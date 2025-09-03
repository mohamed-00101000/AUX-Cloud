#ifndef UART
#define UART

#include <Arduino.h>

#define BUFFER_SIZE 150   // Buffer size for UART
#define BIG_BUFFER_SIZE 600    // Large buffer for URL construction
#define TIMEOUT 1000      // Timeout for UART communication in milliseconds
#define ACK "ACK"         // Acknowledgement response

extern char message[BUFFER_SIZE];             // Store the received message (excluding <S> and <E>)
extern char buffer_uart[BUFFER_SIZE];          // UART buffer to store incoming data
extern char shared_url_buffer[BIG_BUFFER_SIZE];            // Buffer for URL construction
extern int buffer_index;                       // Current position in the UART buffer
extern int message_index;                      // Current position in the message buffer
extern bool end_of_message;                    // Flag for message end
extern bool start_of_message;                  // Flag for message start
extern char data[];                            // Data to send

// Function to receive data via UART
void receive_uart();

// Function to send data to STM
void send_data_to_stm(char *Tx_data);
void send_data_to_pc(char *Tx_data);

#endif
