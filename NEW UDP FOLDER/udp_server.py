import socket
import struct
import json
from datetime import datetime



UDP_IP = "0.0.0.0"       # listens on all interfaces
UDP_PORT = 40000         # must match ESP server_port

PACKET_FORMAT = (
    "<"     # little endian
    "I"     # device_id

    # ---- original STM32 struct ----
    "B"     # start_byte
    "B"     # length
    "H"     # seq

    "f f f"  # left_inv, right_inv, ambient
    "H"      # speed

    "f f f f f"  # lat, lon, yaw_rate, baro, heading_angle
    "B"          # heading_dir

    "f f f f f f" # left_wheel..left_motor
    "f f f f"     # right temps
    "f f f f"     # electrical

    "B B B B"     # indicators

    "B"           # checksum
)


PACKET_SIZE = struct.calcsize(PACKET_FORMAT)



def start():
    print("[INIT] Starting UDP Telemetry Server...")
    print(f"[INIT] Listening on UDP port {UDP_PORT}")
    print(f"[INIT] Expected packet size: {PACKET_SIZE} bytes\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    return sock


def receive_packet(sock):
    data, addr = sock.recvfrom(1024)  # max packet size
    return data, addr


def decode_packet(data):
    if len(data) != PACKET_SIZE:
        return None, f"Invalid packet length: {len(data)}"

    try:
        fields = struct.unpack(PACKET_FORMAT, data)
        return fields, None
    except struct.error as e:
        return None, f"Struct decode error: {e}"


def handle_packet(fields, addr):
    idx = 0

    start_byte = fields[idx]; idx+=1
    length     = fields[idx]; idx+=1
    device_id  = fields[idx]; idx+=1
    seq        = fields[idx]; idx+=1

    left_inv   = fields[idx]; idx+=1
    right_inv  = fields[idx]; idx+=1
    ambient    = fields[idx]; idx+=1
    speed      = fields[idx]; idx+=1

    lat        = fields[idx]; idx+=1
    lon        = fields[idx]; idx+=1
    yaw        = fields[idx]; idx+=1
    baro       = fields[idx]; idx+=1
    head_angle = fields[idx]; idx+=1
    head_dir   = fields[idx]; idx+=1

    left_wheel = fields[idx]; idx+=1
    right_wheel = fields[idx]; idx+=1
    lm1 = fields[idx]; idx+=1
    lm2 = fields[idx]; idx+=1
    lm3 = fields[idx]; idx+=1
    left_motor = fields[idx]; idx+=1

    rm1 = fields[idx]; idx+=1
    rm2 = fields[idx]; idx+=1
    rm3 = fields[idx]; idx+=1
    right_motor = fields[idx]; idx+=1

    volt = fields[idx]; idx+=1
    curr = fields[idx]; idx+=1
    power = fields[idx]; idx+=1
    energy = fields[idx]; idx+=1

    soc = fields[idx]; idx+=1
    tr = fields[idx]; idx+=1
    tl = fields[idx]; idx+=1
    lights = fields[idx]; idx+=1

    checksum = fields[idx]; idx+=1
    
    print(f"\n Packet from {addr}")
    print("---- PACKET: ----")
    print("Device ID:      ", hex(device_id))
    print("Sequence:       ", seq)
    print("Speed:          ", speed)
    print("SOC:            ", soc)
    print("Latitude:       ", lat)
    print("Longitude:      ", lon)
    print("Left Inv Temp:  ", left_inv)
    print("Right Inv Temp: ", right_inv)
    print("Voltage:        ", volt)
    print("Current:        ", curr)
    print("Power:          ", power)
    print("Energy:         ", energy)
    print("-------------------\n")

    save_json(fields)




def save_json(fields):
    # Unpack fields for readability:
    (
        start_byte, length, device_id, seq,

        left_inv, right_inv, ambient, speed,

        lat, lon, yaw, baro, head_angle, head_dir,

        left_wheel, right_wheel, lm1, lm2, lm3, left_motor,

        rm1, rm2, rm3, right_motor,

        volt, curr, power, energy,

        soc, tr, tl, lights, checksum
    ) = fields

    # Format heading direction (your packet stores it as a number)
    heading_direction_string = {
        0: "North",
        1: "North-East",
        2: "East",
        3: "South-East",
        4: "South",
        5: "South-West",
        6: "West",
        7: "North-West"
    }.get(head_dir, "Unknown")

    now = datetime.now()

    json_obj = [{
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),

        "left_inverter_max_temp": left_inv,
        "right_inverter_max_temp": right_inv,
        "ambient_temperature": ambient,
        "car_speed_gauge": speed,

        "lat": lat,
        "lon": lon,
        "yaw_rate": yaw,
        "baro": baro,
        "heading_angle": head_angle,
        "heading_dir": heading_direction_string,

        "left_wheel_spd": left_wheel,
        "right_wheel_spd": right_wheel,
        "left_mosfet_1": lm1,
        "left_mosfet_2": lm2,
        "left_mosfet_3": lm3,
        "left_motor_temp": left_motor,

        "right_mosfet_1": rm1,
        "right_mosfet_2": rm2,
        "right_mosfet_3": rm3,
        "right_motor_temp": right_motor,

        "total_voltage": volt,
        "total_current": curr,
        "power_consumed": power,
        "energy_consumed": energy,

        "soc": soc
    }]

    with open("data.json", "w") as f:
        json.dump(json_obj, f, indent=4)

def main():
    sock = start()

    while True:
        data, addr = receive_packet(sock)

        fields, err = decode_packet(data)
        if err:
            print(f"Decode error from {addr}: {err}")
            continue

        handle_packet(fields, addr)


if __name__ == "__main__":
    main()
