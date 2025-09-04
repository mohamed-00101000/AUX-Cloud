from ftplib import FTP
import io
import json
import time

# FTP credentials and file info
ftp_host = "ftpupload.net"
ftp_user = "if0_38887836"
ftp_pass = "uZnrqJ55D3nN"
ftp_remote_dir = "/htdocs/new"
ftp_filename = "data.json"
local_filename = "data.json"

def download_json_from_ftp():
    try:
        with FTP(ftp_host) as ftp:
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_remote_dir)

            buffer = io.BytesIO()
            ftp.retrbinary(f"RETR {ftp_filename}", buffer.write)

            buffer.seek(0)
            raw_data = buffer.read().decode("utf-8").strip()

            if not raw_data:
                raise ValueError("Downloaded file is empty")

            data = json.loads(raw_data)

            with open(local_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print("Downloaded and saved JSON data:")
            print(json.dumps(data, indent=4))

    except Exception as e:
        print(f"FTP download failed: {e}")

# Loop every 0.5 seconds
while True:
    download_json_from_ftp()
    time.sleep(0.5)