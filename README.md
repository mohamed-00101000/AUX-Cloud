# ASU Racing Team

Welcome to the official repository of the **ASU Racing Team**.  
We are a student-led engineering team working on cutting-edge vehicle systems that combine **embedded systems, cloud computing, and real-time telemetry**.  

This codebase is part of the vehicle that will hit the track in **January 2026**, powering our **Vehicle-to-Cloud communication system** and providing real-time data to the driver and monitoring team.

---

## 📌 About the Project
Our system integrates:
- **STM32 Microcontroller** – Collects raw sensor data from the car (temperature, GPS, voltage, speed, etc.).
- **ESP32 Module** – Manages Wi-Fi and communication with the cloud server.
- **Cloud Scripts** – Stores and serves telemetry for analysis.
- **Desktop Application (Python)** – Used at the station side by engineers to continuously fetch data from the cloud, monitor performance, and support decision-making during testing and races.
- **Dashboard Web Application** – Designed for the driver to monitor real-time data such as speed, temperatures, battery status, and other critical telemetry directly from the vehicle.

    This modular design ensures that both the **driver** and the **station team** have synchronized access to live vehicle data, enabling safe and optimal operation on track.
---

## 📂 Repository Structure

```

.
├── .vscode/            # Development environment settings
├── cloud codes/        # Python/C++ scripts for cloud-side processing
├── Desktop App/        # Monitoring & visualization desktop software
├── docs/               # Documentation and technical reports
├── esp codes/          # ESP32 firmware (Wi-Fi, UART, FTP, JSON handling)
├── web codes/          # PHP/JS/CSS code for the car dashboard web app
├── expected data.txt   # Sample telemetry dataset for testing
└── README.md           # This file

````

---

## ⚙️ Running the System

The system has **two sides**:

### 🚙 Car Side
1. STM32 collects telemetry (speed, temperatures, GPS, etc.).
2. ESP32 receives the data via UART.
3. ESP32 formats the data into JSON and uploads it to the cloud via FTP.

### 🖥️ Station Side
1. A Python script (`getftp.py`) downloads the latest telemetry file from the cloud.
2. Data is parsed into `data.json` and used by:
   - The desktop monitoring app  

---

## 🔧 Getting Started

### Clone the Repository
```bash
git clone https://github.com/aliadelmahdi/AUX-Cloud.git
cd AUX-Cloud
````

### Car Side (ESP32 + STM32)

* Open the `esp codes/` folder in Arduino IDE or PlatformIO.
* Configure Wi-Fi SSID and password in the ESP32 firmware.
* Flash the firmware to the ESP32.

### Station Side (Monitoring App)

* Navigate to `cloud codes/`.

* Run the monitoring script:

  ```bash
  python getftp.py
  ```

### Dashboard

* Upload the contents of `web codes/` to your web server.
* Ensure `data.json` is being updated from the FTP server.
* Open the dashboard in your browser to monitor telemetry live.

---

## 📅 Road to 2026

This system is under continuous development and will be **deployed in our racing vehicle for the January 2026 competition**.
Stay tuned for updates as we refine performance, reliability, and cloud integration.

---

## 📜 License

This project is developed for research, competition, and educational purposes under the ASU Racing Team.
Usage outside the team should respect proper attribution.

---