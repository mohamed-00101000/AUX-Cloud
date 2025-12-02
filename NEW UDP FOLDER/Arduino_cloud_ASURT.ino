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

TelemetryPacket pkt;
uint16_t seq_counter = 0;

// Simulated SOC value
float soc_value = 100.0;

// ---------------- Checksum ----------------
uint8_t compute_checksum(uint8_t* data, uint16_t len) {
    uint8_t sum = 0;
    for (uint16_t i = 0; i < len; i++) {
        sum ^= data[i];
    }
    return sum;
}

// ---------------- Fill Packet ----------------
void fill_sample_telemetry(TelemetryPacket &p) {

    p.start_byte = 0xAA;
    p.seq = seq_counter++;

    // your static test values
    p.left_inverter_max_temp  = 32.5f;
    p.right_inverter_max_temp = 32.5f;
    p.ambient_temperature     = 28.0f;
    p.car_speed_gauge         = 40;
    p.lat                     = 25.87f;
    p.lon                     = 30.799999f;
    p.yaw_rate                = 7.34f;
    p.baro                    = 1038.23f;
    p.heading_angle           = 208.84f;
    p.heading_dir             = 3;

    p.left_wheel_spd          = 58.18f;
    p.right_wheel_spd         = 57.36f;
    p.left_mosfet_1           = 65.15f;
    p.left_mosfet_2           = 68.49f;
    p.left_mosfet_3           = 67.65f;
    p.left_motor_temp         = 75.45f;

    p.right_mosfet_1          = 91.09f;
    p.right_mosfet_2          = 84.41f;
    p.right_mosfet_3          = 91.34f;
    p.right_motor_temp        = 82.72f;

    p.total_voltage           = 105.12f;
    p.total_current           = 4.34f;
    p.power_consumed          = 13.92f;
    p.energy_consumed         = 35.69f;

    // ---- UPDATE SOC ----
    soc_value -= 0.1;       // decrease slowly
    if (soc_value < 0) soc_value = 100.0;   // reset back to 100

    p.soc = (uint8_t)soc_value;

    p.turnright = 1;
    p.turnleft = 1;
    p.lights_v1 = 1;

    p.length = sizeof(TelemetryPacket);

    p.checksum = compute_checksum((uint8_t*)&p, sizeof(TelemetryPacket) - 1);
}

// ---------------- UART Send ----------------
void send_telemetry() {
    fill_sample_telemetry(pkt);
    Serial.write((uint8_t*)&pkt, sizeof(TelemetryPacket));
}

void setup() {
    Serial.begin(115200);
    delay(2000);
}

void loop() {
    send_telemetry();
    delay(100);
}