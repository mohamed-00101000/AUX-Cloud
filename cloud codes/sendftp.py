import random
import time
import json
import io
from datetime import datetime
from ftplib import FTP

# FTP Configuration
ftp_host = "ftpupload.net"
ftp_user = "if0_38887836"
ftp_pass = "uZnrqJ55D3nN"
ftp_remote_file = "data.json"
ftp_remote_dir = "/htdocs/new"

def upload_to_ftp(json_content):
    try:
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_remote_dir)
            ftp.storbinary(f"STOR {ftp_remote_file}", io.BytesIO(json_content.encode("utf-8")))
            print("Uploaded to FTP")
    except Exception as e:
        print(f"FTP upload failed: {str(e)}")

counter = 0

while True:
    now = datetime.now()
    data = {
        "date": now.strftime('%Y-%m-%d'),
        "time": now.strftime('%H:%M:%S'),
        "left_inverter_max_temp": round(random.uniform(80, 100), 2),
        "right_inverter_max_temp": round(random.uniform(80, 100), 2),
        "ambient_temperature": round(random.uniform(20, 40), 2),
        "car_speed_gauge": counter,
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

    json_string = json.dumps([data], indent=4)
    print(f"SOC: {data['soc']}")  # Print SOC value
    upload_to_ftp(json_string)

    counter = (counter + 1) % 100
    time.sleep(0.5)
