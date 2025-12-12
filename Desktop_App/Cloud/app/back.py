from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import json
import sys
import time

from app.front import Ui_MainWindow
from app.Battery import BatteryWidget
from app.Speed_Gauge import CarGaugeWidget
from app.GPS import GPSMapWidget


# ============================================================
# BACKGROUND JSON READER
# ============================================================
class JSONWorker(QThread):
    update_signal = pyqtSignal(dict)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        while True:
            try:
                with open(self.file_path, "r") as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    variables = data
                elif isinstance(data, list):
                    variables = data[0] if len(data) > 0 else {}
                else:
                    variables = {}

                self.update_signal.emit(variables)

            except Exception as e:
                print(f"[JSONWorker] Error:", e)

            time.sleep(0.5)



# ============================================================
# BACK-END CLASS
# ============================================================
class BackEndClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Hide tab bar for cleaner GUI
        self.tabWidget.tabBar().setVisible(False)

        # Initialize widgets
        self.setup_car_speed_widgets()
        self.setup_battery_widget()
        self.setup_gps_map()

        # Connect menu buttons
        self.Thermal_Button.clicked.connect(self.Thermal)
        self.Electrical_Button.clicked.connect(self.Electrical)
        self.Physical_Button.clicked.connect(self.Physical)

        self.back_btn_from_Thermal.clicked.connect(self.back_menu)
        self.back_btn_from_Electrical.clicked.connect(self.back_menu)
        self.back_btn_from_Physical.clicked.connect(self.back_menu)

        # Start JSON worker
        json_path = Path(__file__).parent / "data" / "data.json"
        self.json_worker = JSONWorker(json_path)
        self.json_worker.update_signal.connect(self.update_from_json)
        self.json_worker.start()



    # ============================================================
    # UI SETUP FUNCTIONS
    # ============================================================
    def setup_car_speed_widgets(self):

        # Car Speed
        if self.CarSpeed_widget.layout() is None:
            self.CarSpeed_widget.setLayout(QtWidgets.QVBoxLayout())

        self.car_speed_widget = CarGaugeWidget(self)
        self.CarSpeed_widget.layout().addWidget(self.car_speed_widget)

        # Right wheel
        if self.RightWheelSpeed_widget.layout() is None:
            self.RightWheelSpeed_widget.setLayout(QtWidgets.QVBoxLayout())

        self.right_wheel_speed_widget = CarGaugeWidget(self)
        self.RightWheelSpeed_widget.layout().addWidget(self.right_wheel_speed_widget)

        # Left wheel
        if self.LeftWheelSpeed_widget.layout() is None:
            self.LeftWheelSpeed_widget.setLayout(QtWidgets.QVBoxLayout())

        self.left_wheel_speed_widget = CarGaugeWidget(self)
        self.LeftWheelSpeed_widget.layout().addWidget(self.left_wheel_speed_widget)



    def setup_battery_widget(self):

        if self.Battery_widget.layout() is None:
            self.Battery_widget.setLayout(QtWidgets.QVBoxLayout())

        self.battery_widget = BatteryWidget()
        self.Battery_widget.layout().addWidget(self.battery_widget)



    def setup_gps_map(self):

        if self.GPS_widget.layout() is None:
            self.GPS_widget.setLayout(QtWidgets.QVBoxLayout())

        self.gps_widget = GPSMapWidget()   # NEW GPS version takes NO arguments
        self.GPS_widget.layout().addWidget(self.gps_widget)



    # ============================================================
    # UPDATE UI FROM JSON
    # ============================================================
    def update_from_json(self, v):
        try:
            # Map internal class variables to JSON keys
            mapping = {
                "Overall_Car_Speed": "car_speed_gauge",
                "Left_Wheel_Speed": "left_wheel_spd",
                "Right_Wheel_Speed": "right_wheel_spd",
                "Yaw_rate": "yaw_rate",
                "barometer": "baro",
                "Car_heading_Angle": "heading_angle",
                "Car_heading_Dir": "heading_dir",
                "Left_Inverter_Max_Temp": "left_inverter_max_temp",
                "Right_Inverter_Max_Temp": "right_inverter_max_temp",
                "Ambient_temp": "ambient_temperature",
                "Left_MOSFETs_Temp1": "left_mosfet_1",
                "Left_MOSFETs_Temp2": "left_mosfet_2",
                "Left_MOSFETs_Temp3": "left_mosfet_3",
                "Right_MOSFETs_Temp1": "right_mosfet_1",
                "Right_MOSFETs_Temp2": "right_mosfet_2",
                "Right_MOSFETs_Temp3": "right_mosfet_3",
                "Left_Motor_Temp": "left_motor_temp",
                "Right_Motor_Temp": "right_motor_temp",
                "Total_Voltage": "total_voltage",
                "Total_Current": "total_current",
                "Power_Consumed": "power_consumed",
                "Energy_Consumed": "energy_consumed",
                "SOC": "soc",
            }

            # Read & convert values
            for attr, json_key in mapping.items():
                raw = v.get(json_key, None)

                if attr == "Car_heading_Dir":   # string case
                    setattr(self, attr, raw if raw is not None else "Unknown")
                else:
                    try:
                        setattr(self, attr, float(raw))
                    except:
                        setattr(self, attr, 0.0)

            # Update gauges
            self.car_speed_widget.setValue(self.Overall_Car_Speed)
            self.left_wheel_speed_widget.setValue(self.Left_Wheel_Speed)
            self.right_wheel_speed_widget.setValue(self.Right_Wheel_Speed)

            # Update LCDs
            self.Yaw_Lcd.display(self.Yaw_rate)
            self.Barometer_lcd.display(self.barometer)

            self.textBrowser_Headings_Angle.setText(str(self.Car_heading_Angle))
            self.textBrowser_Headings_Litter.setText(self.Car_heading_Dir)

            self.left_inverter_max_temp_lcd.display(self.Left_Inverter_Max_Temp)
            self.right_inverter_max_temp_lcd.display(self.Right_Inverter_Max_Temp)
            self.Ambient_temp_lcd.display(self.Ambient_temp)

            self.Left_Mosfets_temp_1_lcd.display(self.Left_MOSFETs_Temp1)
            self.Left_Mosfets_temp_2_lcd.display(self.Left_MOSFETs_Temp2)
            self.Left_Mosfets_temp_3_lcd.display(self.Left_MOSFETs_Temp3)
            self.Right_Mosfets_temp_1_lcd.display(self.Right_MOSFETs_Temp1)
            self.Right_Mosfets_temp_2_lcd.display(self.Right_MOSFETs_Temp2)
            self.Right_Mosfets_temp_3_lcd.display(self.Right_MOSFETs_Temp3)
            self.Left_Motor_temp_lcd.display(self.Left_Motor_Temp)
            self.Right_Motor_temp_lcd.display(self.Right_Motor_Temp)

            self.Total_Voltage_lcd.display(self.Total_Voltage)
            self.Total_Current_lcd.display(self.Total_Current)
            self.Power_Consumed_lcd.display(self.Power_Consumed)
            self.Energy_Consumed_lcd.display(self.Energy_Consumed)

            # Battery
            self.battery_widget.set_battery_level(self.SOC)

            # GPS update
            lat = v.get("lat")
            lon = v.get("lon")

            if lat is not None and lon is not None:
                try:
                    self.gps_widget.update_vehicle_position(float(lat), float(lon))
                except:
                    print("[GPS] Invalid lat/lon")

        except Exception as e:
            print("[UI ERROR] update_from_json:", e)


    # ============================================================
    # PAGE NAVIGATION
    # ============================================================
    def Thermal(self):
        self.tabWidget.setCurrentIndex(1)

    def Electrical(self):
        self.tabWidget.setCurrentIndex(2)

    def Physical(self):
        self.tabWidget.setCurrentIndex(3)

    def back_menu(self):
        self.tabWidget.setCurrentIndex(0)



# ============================================================
# APP ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BackEndClass()
    win.show()
    sys.exit(app.exec_())
