import random
import requests
from datetime import datetime
from urllib.parse import urlencode
import time

# Configuration
max_retries = 3
retry_delay = 2
log_file_path = "error_log_send.txt"
send_count = 0
error_count = 0
start_time = time.time()
counter = 0

# Headers to look like a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html,application/xhtml+xml',
    'Connection': 'keep-alive'
}

def log_message(message, include_timestamp=True):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        if include_timestamp:
            log_file.write(f"{time.ctime()}: {message}\n")
        else:
            log_file.write(f"{message}\n")

def send_data_with_retries(data):
    global send_count, error_count, start_time
    base_url = "https://racingteam.rf.gd/new/add.php"
    attempt = 0

    while attempt < max_retries:
        try:
            url_with_params = f"{base_url}?{urlencode(data)}"
            print(f"[Sending] {url_with_params}")

            response = requests.get(url_with_params, headers=headers, timeout=10)
            response.raise_for_status()

            send_count += 1
            elapsed_time = time.time() - start_time
            log_message(f"Successful send #{send_count}")
            return True

        except Exception as e:
            error_count += 1
            elapsed_time = time.time() - start_time
            log_message(f"Error #{error_count}")
            log_message(f"Time taken for error: {elapsed_time / 60:.2f} minutes")
            log_message(f"Exception: {repr(e)}")
            start_time = time.time()
            attempt += 1
            time.sleep(retry_delay)

    return False

log_message(f"Start Time: {time.ctime()}", include_timestamp=False)

while True:
    current_datetime = datetime.now()
    date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S')

    data = {
        "date": date,
        "time": current_time,
        "left_inverter_max_temp": round(random.uniform(80, 100), 2),
        "right_inverter_max_temp": round(random.uniform(80, 100), 2),
        "ambient_temperature": round(random.uniform(20, 40), 2),
        "car_speed_gauge": round(random.uniform(0, 80), 2),
        "lat": round(random.uniform(45.0, 46.0), 6),
        "lon": round(random.uniform(-2.0, -1.0), 6),
        "yaw_rate": round(random.uniform(0, 30), 2),
        "baro": round(random.uniform(950, 1050), 2),
        "heading_angle": round(random.uniform(0, 360), 2),
        "heading_dir": random.choice(["North", "South", "East", "West", "North-East", "South-West"]),
        "left_wheel_spd": round(random.uniform(50, 60), 2),
        "right_wheel_spd": round(random.uniform(50, 60), 2),
        "left_mosfet_1": round(random.uniform(60, 70), 2),
        "left_mosfet_2": round(random.uniform(60, 70), 2),
        "left_mosfet_3": round(random.uniform(60, 70), 2),
        "left_motor_temp": round(random.uniform(70, 80), 2),
        "right_mosfet_1": round(random.uniform(80, 95), 2),
        "right_mosfet_2": round(random.uniform(80, 95), 2),
        "right_mosfet_3": round(random.uniform(80, 95), 2),
        "right_motor_temp": round(random.uniform(80, 90), 2),
        "total_voltage": round(random.uniform(100, 110), 2),
        "total_current": round(random.uniform(4, 6), 2),
        "power_consumed": round(random.uniform(10, 15), 2),
        "energy_consumed": round(random.uniform(30, 40), 2),
        "soc": counter
    }

    send_data_with_retries(data)

    counter += 1
    if counter >= 100:
        counter = 0

    time.sleep(15)
