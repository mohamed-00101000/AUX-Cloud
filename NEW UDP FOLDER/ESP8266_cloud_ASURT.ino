#include <WiFiUdp.h>
#include <ESP8266WiFi.h>


#define START_BYTE 0xAA

// ------------ WiFi Credentials -----------
const char* ssid = "saif_2.4GEXT";
const char* password = "*saif#2023";

const char* serverIP = "192.168.1.4";   // TEMP: laptop IP for testing
int server_port = 40000;                 

// ------------ UDP transport layer  ----------------
WiFiUDP udp;
const uint32_t deviceID = 0xAFA123AF;   // choose any unique 32-bit value


// -------------- packet structure ---------------
typedef struct __attribute__((packed)) {

    uint8_t  start_byte;
    uint8_t  length;
    uint16_t seq;

    float left_inverter_max_temp;
    float right_inverter_max_temp;
    float ambient_temperature;
    uint16_t car_speed_gauge;
    float lat;
    float lon;
    float yaw_rate;
    float baro;
    float heading_angle;
    uint8_t heading_dir;

    float left_wheel_spd;
    float right_wheel_spd;
    float left_mosfet_1;
    float left_mosfet_2;
    float left_mosfet_3;
    float left_motor_temp;

    float right_mosfet_1;
    float right_mosfet_2;
    float right_mosfet_3;
    float right_motor_temp;

    float total_voltage;
    float total_current;
    float power_consumed;
    float energy_consumed;

    uint8_t soc;
    uint8_t turnright;
    uint8_t turnleft;
    uint8_t lights_v1;

    uint8_t checksum;

} TelemetryPacket;


typedef struct __attribute__((packed)) {
    uint32_t device_id; 
    TelemetryPacket data;
} UdpPacket;



// -------- CHECKSUM ----------
uint8_t compute_checksum(uint8_t *data, uint16_t len) {
    uint8_t sum = 0;
    for (uint16_t i = 0; i < len; i++) {
        sum ^= data[i];
    }
    return sum;
}


// -------- UART STATE MACHINE ----------
enum RxState { WAIT_START, WAIT_LENGTH, WAIT_PAYLOAD };
RxState rx_state = WAIT_START;

uint8_t  rx_buffer[256];
uint16_t rx_index = 0;
uint16_t expected_length = 0;

TelemetryPacket decodedPacket;


// -------- UART RECEIVER ----------
bool receive_uart_packet() {

    while (Serial.available()) {

        uint8_t b = Serial.read();

        switch (rx_state) {

            case WAIT_START:
                if (b == START_BYTE) {
                    rx_buffer[0] = b;
                    rx_index = 1;
                    rx_state = WAIT_LENGTH;
                }
                break;

            case WAIT_LENGTH:
                expected_length = b;
                rx_buffer[1] = b;
                rx_index = 2;

                if (expected_length < 30 || expected_length > 200) {
                    rx_state = WAIT_START;
                    break;
                }

                rx_state = WAIT_PAYLOAD;
                break;

            case WAIT_PAYLOAD:
                rx_buffer[rx_index++] = b;

                if (rx_index == expected_length) {
                    uint8_t received_checksum = rx_buffer[expected_length - 1];
                    uint8_t calculated_checksum = compute_checksum(rx_buffer, expected_length - 1);

                    if (received_checksum == calculated_checksum) {
                        memcpy(&decodedPacket, rx_buffer, expected_length);
                        // decodedPacket.device_id = deviceID;
                        // decodedPacket.length = sizeof(TelemetryPacket);
                        rx_state = WAIT_START;
                        return true;
                    } else {
                        rx_state = WAIT_START;
                        return false;
                    }
                }
                break;
        }
    }

    return false;
}


// -------- SEND UDP PACKET FUNCTION -------------
void send_udp_packet() {
    UdpPacket pkt;

    pkt.device_id = deviceID;
    memcpy(&pkt.data, &decodedPacket, sizeof(TelemetryPacket));

    udp.beginPacket(serverIP, server_port);
    udp.write((uint8_t*)&pkt, sizeof(pkt));
    udp.endPacket();
}




void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    Serial.println("Connecting WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(300);
        Serial.print(".");
    }

    Serial.println("\nWiFi Connected.");
    udp.begin(12345);
}


void loop() {

    if (receive_uart_packet()) {
        Serial.println("VALID PACKET RECEIVED");
        send_udp_packet();
    }
}