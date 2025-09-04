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
ftp_remote_file = "driver.json"
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
        "number_of_labs": counter
    }

    json_string = json.dumps([data], indent=4)
    print(f"number_of_labs: {data['number_of_labs']}")  # Print number_of_labs value
    upload_to_ftp(json_string)

    counter = (counter + 1) % 15
    time.sleep(0.5)
