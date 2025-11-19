    #include "uart.h"
    #include "JSONParser.h"
    #include "HTTPRequest.h"
    #include "SendFTP.h"

    char message[BUFFER_SIZE];              // Store the received message (excluding <S> and <E>)
    char buffer_uart[BUFFER_SIZE];          // UART buffer to store incoming data
    char shared_url_buffer[BIG_BUFFER_SIZE];// Buffer for URL construction
    int buffer_index = 0;                   // Current position in the UART buffer
    int message_index = 0;                  // Current position in the message buffer
    bool end_of_message = false;            // Flag for message end
    bool start_of_message = false;          // Flag for message start
    char data[] = "<S>ID_1:32.5,ID_2:32.5,ID_3:28.0,ID_4:45.0,ID_5:30.0,ID_6:30.0<E>";  // Sample data
    char buffer[32];                        // Temporary buffer



    void receive_uart() {
        while (Serial.available() > 0) {
            char receivedChar = Serial.read();  // Read a single character from UART
            // Serial.println(receivedChar);
            // Store data in the UART buffer
            buffer_uart[buffer_index++] = receivedChar;
            // Check for the start delimiter "<S>"
            if (buffer_index >= 4 && buffer_uart[buffer_index - 2] == '>' && buffer_uart[buffer_index - 3] == 'S' && buffer_uart[buffer_index - 4] == '<') {
                start_of_message = true;
                message_index = 0;  // Reset message index to start storing message
                buffer_index = 0;   // Reset UART buffer index after start delimiter
            }
            
            // Check for the end delimiter "<E>"
            if (buffer_index >= 3 && buffer_uart[buffer_index - 1] == '>' && buffer_uart[buffer_index - 2] == 'E' && buffer_uart[buffer_index - 3] == '<') {
                end_of_message = true;
            }
            
            // If we are in a valid message, store characters in the message array, skipping '<' and '>'
            if (start_of_message && !end_of_message) {
                message[message_index++] = receivedChar;  // Store character in the message array
            }
            
            // If the end delimiter is found, stop storing and print the message
            if (start_of_message && end_of_message) {
                message[message_index] = '\0';  // Null-terminate the message string
                message[message_index-1] = '\0';
                message[message_index-2] = '\0';
                // Serial.println("Received buffer:");
                // Serial.println(buffer_uart);  
                // Print the received message
                
                Serial.println(message);  // Print the message without the <S> and <E> markers



                
                parseFrame(String(message));
                // pressLink(generateURL());
                
                // Reset flags and buffers for the next message
                start_of_message = false;
                end_of_message = false;
                buffer_index = 0;  // Reset the UART buffer index
                message_index = 0; // Reset the message index
            }
        }
    }

    void send_data_to_stm(char *Tx_data) {
        unsigned long lastTime;  // To track time
        char received[32];       // Buffer to hold the response

        do {
            Serial.println(data);  // Sending sample data
            // Wait for the response
            lastTime = millis();  // Capture the current time
            bool ack_received = false;

            while (millis() - lastTime < TIMEOUT) {
                if (Serial.available()) {
                    size_t len = Serial.readBytesUntil('\n', received, sizeof(received) - 1);
                    received[len] = '\0'; // Null-terminate the received string
                    if (strcmp(received, ACK) == 0) {
                        ack_received = true;
                        break;
                    }
                }
            }
            if (ack_received) {
                break; // Exit loop if ACK received
            }

        } while (true);
    }

    void send_data_to_pc(char *Tx_data) {
            Serial.println(Tx_data);  // Sending sample data
    }