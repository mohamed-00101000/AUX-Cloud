import random
import requests
from datetime import datetime
from urllib.parse import urlencode
import time
import json
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError, Timeout, RequestException
import sys

# Configuration
max_retries = 3  # Max retries for sending data
retry_delay = 2  # Delay between retries
log_file_path = "error_log_send.txt"  # Log file path
# delay =1
delay = int(sys.argv[2])

# Counters
send_count = 0
error_count = 0
start_time = time.time()  # Use time.time() to get a numeric timestamp for elapsed time
counter = 0
# Function to log messages to a file
def log_message(message, include_timestamp=True):
    with open(log_file_path, 'a') as log_file:
        if include_timestamp:
            log_file.write(f"{time.ctime()}: {message}\n")
        else:
            log_file.write(f"{message}\n")

# Function to send data with retries
def send_data_with_retries(data):
    global send_count, error_count, start_time
    attempt = 0
    while attempt < max_retries:
        try:
            
            # Construct the URL with query parameters
            # base_url = "https://racingteam.rf.gd/new/add.php"#مجانية
            # base_url = "https://projectegypt.online/new/add.php"# المدفوعة
            base_url = sys.argv[1]
            print(f"Send base_url: {base_url}, delay: {delay}")

            url_with_params = f"{base_url}?{urlencode(data)}"
            print(url_with_params);
            # Send a GET request to the generated URL
            # response = requests.get(url_with_params, timeout=200)
            # response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

            # Increment the send counter and log success
            send_count += 1
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            log_message(f"Successful send #{send_count}")
            return True

        except Exception as e:
            # Increment the error counter and log the error
            error_count += 1
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            log_message(f"Error #{error_count}")
            log_message(f"Time taken to get an error #{elapsed_time / 60:.2f} minutes")
            start_time = time.time()  # Reset start time to current time
            return False


# Log the start time without timestamp
log_message(f"Start Time: {time.ctime()}", include_timestamp=False)

# Main loop
while True:
    # Generate current date and time
    current_datetime = datetime.now()
    date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S')  # Rename 'time' to 'current_time'

    # Random data for the fields
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
    
    #Attempt to send data with retries
    send_data_with_retries(data)
    counter= counter+1
    if(counter==100):
        counter=0
    # Delay before the next iteration
    time.sleep(delay)