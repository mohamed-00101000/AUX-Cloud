from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import json
import sys
import time
from Battery import BatteryWidget
from Speed_Gauge import CarGaugeWidget
from front import Ui_MainWindow  # Ensure this import is correct and Ui_MainWindow is properly defined
from GPS import GPSMapWidget

class JSONWorker(QThread):
    update_signal = pyqtSignal(dict)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        while True:
            try:
                # Read and parse the JSON file
                with open(self.file_path, 'r') as file:
                    data = json.load(file)

                # Ensure data is a dictionary or handle lists appropriately
                if isinstance(data, list):
                    variables = data[0] if len(data) > 0 else {}
                elif isinstance(data, dict):
                    variables = data
                else:
                    raise ValueError("Unexpected JSON structure")

                # Emit the data
                self.update_signal.emit(variables)
            except Exception as e:
                print(f"Error reading JSON file: {e}")
            time.sleep(1)  # Update every second


# BackEndClass modified to use JSONWorker for all updates
class BackEndClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.left_wheel_speed_widget = None
        self.right_wheel_speed_widget = None
        self.car_speed_widget = None
        self.battery_widget = None
        self.gps_widget = None  # Add a variable to hold the GPS widget
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False)

        # Setup widgets
        self.setup_car_speed_widgets()
        self.setup_battery_widget()
        self.setup_gps_map()  # Initialize GPS map widget once

        # Connect buttons to their respective functions
        self.Thermal_Button.clicked.connect(self.Thermal)
        self.Electrical_Button.clicked.connect(self.Electrical)
        self.Physical_Button.clicked.connect(self.Physical)
        self.back_btn_from_Thermal.clicked.connect(self.back_menu)
        self.back_btn_from_Electrical.clicked.connect(self.back_menu)
        self.back_btn_from_Physical.clicked.connect(self.back_menu)

        # Start background worker for JSON data
        json_file_path = "data.json"  # Update with your JSON file path
        self.json_worker = JSONWorker(json_file_path)
        self.json_worker.update_signal.connect(self.update_from_json)
        self.json_worker.start()

    def update_from_json(self, variables):
        try:
            # Map JSON keys to variables and their default values
            data_mapping = {
                "Overall_Car_Speed": ("car_speed_gauge", 0.0),
                "Left_Wheel_Speed": ("left_wheel_spd", 0.0),
                "Right_Wheel_Speed": ("right_wheel_spd", 0.0),
                "Yaw_rate": ("yaw_rate", 0.0),
                "barometer": ("baro", 0.0),
                "Car_heading_Angle": ("heading_angle", 0.0),
                "Car_heading_Dir": ("heading_dir", ""),  # Keep this as a string
                "Left_Inverter_Max_Temp": ("left_inverter_max_temp", 0.0),
                "Right_Inverter_Max_Temp": ("right_inverter_max_temp", 0.0),
                "Ambient_temp": ("ambient_temperature", 0.0),
                "Left_MOSFETs_Temp1": ("left_mosfet_1", 0.0),
                "Left_MOSFETs_Temp2": ("left_mosfet_2", 0.0),
                "Left_MOSFETs_Temp3": ("left_mosfet_3", 0.0),
                "Right_MOSFETs_Temp1": ("right_mosfet_1", 0.0),
                "Right_MOSFETs_Temp2": ("right_mosfet_2", 0.0),
                "Right_MOSFETs_Temp3": ("right_mosfet_3", 0.0),
                "Left_Motor_Temp": ("left_motor_temp", 0.0),
                "Right_Motor_Temp": ("right_motor_temp", 0.0),
                "Total_Voltage": ("total_voltage", 0.0),
                "Total_Current": ("total_current", 0.0),
                "Power_Consumed": ("power_consumed", 0.0),
                "Energy_Consumed": ("energy_consumed", 0.0),
                "SOC": ("soc", 0.0),
            }

            # Update values dynamically
            for attr, (key, default) in data_mapping.items():
                value = variables.get(key, None)

                # Handle specific case for heading_dir (string value)
                if key == "Car_heading_Dir":
                    setattr(self, attr, value)  # Keep as a string
                else:
                    # Try converting to float, if fails, keep default value
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        value = default
                    setattr(self, attr, value)

            # Update GUI components directly
            self.car_speed_widget.setValue(self.Overall_Car_Speed)
            self.left_wheel_speed_widget.setValue(self.Left_Wheel_Speed)
            self.right_wheel_speed_widget.setValue(self.Right_Wheel_Speed)
            self.Yaw_Lcd.display(self.Yaw_rate)
            self.Barometer_lcd.display(self.barometer)
            self.textBrowser_Headings_Angle.setText(str(self.Car_heading_Angle))
            heading_dir = variables.get("heading_dir", "Unknown")  # Default to "Unknown"
            self.textBrowser_Headings_Litter.setText(heading_dir)
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
            self.battery_widget.set_battery_level(self.SOC)

            lat = variables.get("lat", None)
            lon = variables.get("lon", None)

            if lat is not None and lon is not None:
                try:
                    lat = float(lat)
                    lon = float(lon)
                    self.gps_widget.update_vehicle_position(lat, lon)
                except Exception as e:
                    print("[GPS] Failed to update:", e)

        except KeyError as e:
            print(f"Missing key in JSON: {e}")
        except ValueError as e:
            print(f"Invalid value in JSON: {e}")
        except Exception as e:
            print(f"Error updating from JSON: {e}")

    def setup_gps_map(self):

        # Set up the GPS map widget
        self.gps_widget = GPSMapWidget([])

        # Set the layout and geometry if necessary
        self.GPS_widget.setLayout(QtWidgets.QVBoxLayout())  # Ensure there is a layout
        self.GPS_widget.layout().addWidget(self.gps_widget)  # Add the GPS widget to your existing GPS widget
        self.GPS_widget.setGeometry(0, 0, 600, 300)  # Adjust as necessary
        self.GPS_widget.show()  # Optionally show if not visible


    def setup_car_speed_widgets(self):
        # Set up CarSpeed_widget
        if self.CarSpeed_widget.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.CarSpeed_widget)
            self.CarSpeed_widget.setLayout(layout)

        self.car_speed_widget = CarGaugeWidget(self)
        self.CarSpeed_widget.layout().addWidget(self.car_speed_widget)

        # Set up RightWheelSpeed_widget
        if self.RightWheelSpeed_widget.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.RightWheelSpeed_widget)
            self.RightWheelSpeed_widget.setLayout(layout)

        self.right_wheel_speed_widget = CarGaugeWidget(self)
        self.RightWheelSpeed_widget.layout().addWidget(self.right_wheel_speed_widget)

        # Set up LeftWheelSpeed_widget
        if self.LeftWheelSpeed_widget.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.LeftWheelSpeed_widget)
            self.LeftWheelSpeed_widget.setLayout(layout)

        self.left_wheel_speed_widget = CarGaugeWidget(self)
        self.LeftWheelSpeed_widget.layout().addWidget(self.left_wheel_speed_widget)

    def setup_battery_widget(self):
        if self.Battery_widget.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.Battery_widget)
            self.Battery_widget.setLayout(layout)

        self.battery_widget = BatteryWidget()
        self.Battery_widget.layout().addWidget(self.battery_widget)

    def Thermal(self):
        self.tabWidget.setCurrentIndex(1)

    def Electrical(self):
        self.tabWidget.setCurrentIndex(2)

    def Physical(self):
        self.tabWidget.setCurrentIndex(3)

    def back_menu(self):
        self.tabWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # gps_data_file = r"C:\Users\HP\Desktop\Shell track coordinates\sem_apme_2025-track_coordinates.csv"
    # gps_coords = load_track_data(gps_data_file)
    # if not gps_coords:
    #     print("No valid GPS data found.")
    #     sys.exit(1)

    main_window = BackEndClass()
    main_window.show()
    sys.exit(app.exec_())
