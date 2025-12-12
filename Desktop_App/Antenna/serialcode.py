

"speed =15 , lat = 50.848448 ,soc = 80 , voltage"



import serial

# Set the correct COM port based on Device Manager (adjust as needed)
SERIAL_PORT = 'COM4'  # Change to your COM port, e.g., 'COM5', 'COM6', etc.
SERIAL_RATE = 9600  # Ensure this matches the baud rate of your device


def Read_From_Serial():
    try:
        # Open the serial port with a 1-second timeout
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {SERIAL_RATE} baud.")

        while True:
            if ser.in_waiting > 0:  # Check if there is data to read
                # Read the incoming string, decode it, and strip newline characters
                reading = ser.readline().decode('utf-8', errors='ignore').rstrip()
                print(f"Data received: {reading}")

    except serial.SerialException as e:
        print(f"Error opening serial port {SERIAL_PORT}: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()  # Ensure the serial port is closed on exit
            print("Serial port closed.")


if __name__ == "__main__":
    Read_From_Serial()



#
# import serial
#
# # Set the correct COM port based on Device Manager (adjust as needed)
# SERIAL_PORT = 'COM4'  # Change to your COM port, e.g., 'COM5', 'COM6', etc.
# SERIAL_RATE = 9600  # Ensure this matches the baud rate of your device
#
# # Define a list of variable names for easier management
# VARIABLE_NAMES = [
#     "Left_Inverter_Maximum_Temperature",
#     "Right_Inverter_Maximum_Temperature",
#     "Ambient_Temperature",
#     "Car_Overall_Speed_Gauge",
#     "Longitude",
#     "Latitude",
#     "Number_Of_Laps",
#     "Maximum_Inverter_Temperature",
#     "YawRate",
#     "Barometer_Reading",
#     "Car_heading_angle",
#     "Car_heading_direction",
#     "Left_Wheel_Speed",
#     "Right_Wheel_Speed",
#     "Left_MOSFETS_Temperature1",
#     "Left_MOSFETS_Temperature2",
#     "Left_MOSFETS_Temperature3",
#     "Left_Motor_Temperature",
#     "Right_MOSFETS_Temperature1",
#     "Right_MOSFETS_Temperature2",
#     "Right_MOSFETS_Temperature3",
#     "Right_Motor_Temperature",
#     "Total_Voltage",
#     "Total_Current",
#     "Power_Consumed",
#     "Energy_Consumed",
#     "SOC"
# ]
#
# EXPECTED_VARIABLES = len(VARIABLE_NAMES)
#
# def parse_data(reading):
#     """
#     Parses the serial input data into variables.
#     Handles both delimited and non-delimited formats.
#     """
#     # Check if data contains commas
#     if "," in reading:
#         # Split by commas
#         data = reading.split(",")
#     else:
#         # Assume fixed-width splitting for non-delimited input
#         if len(reading) % EXPECTED_VARIABLES == 0:
#             # Calculate segment size
#             segment_size = len(reading) // EXPECTED_VARIABLES
#             data = [reading[i:i + segment_size] for i in range(0, len(reading), segment_size)]
#         else:
#             print(f"Error: Data length {len(reading)} does not match expected number of variables.")
#             return None
#
#     if len(data) == EXPECTED_VARIABLES:
#         try:
#             # Map variable names to values and return as a dictionary
#             parsed_data = dict(zip(VARIABLE_NAMES, map(float, data)))
#             return parsed_data
#         except ValueError as e:
#             print(f"Error converting data to float: {e}")
#             return None
#     else:
#         print(f"Error: Expected {EXPECTED_VARIABLES} values, but got {len(data)}.")
#         return None
#
#
# def Read_From_Serial():
#     try:
#         # Open the serial port with a 1-second timeout
#         ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
#         print(f"Connected to {SERIAL_PORT} at {SERIAL_RATE} baud.")
#
#         while True:
#             if ser.in_waiting > 0:  # Check if there is data to read
#                 # Read the incoming string, decode it, and strip newline characters
#                 reading = ser.readline().decode('utf-8', errors='ignore').rstrip()
#                 print(f"Data received: {reading}")
#
#                 # Parse the data
#                 parsed_data = parse_data(reading)
#                 if parsed_data:
#                     print("Parsed Data:")
#                     for key, value in parsed_data.items():
#                         print(f"{key}: {value}")
#
#     except serial.SerialException as e:
#         print(f"Error opening serial port {SERIAL_PORT}: {e}")
#
#     except Exception as e:
#         print(f"Error: {e}")
#
#     finally:
#         if 'ser' in locals() and ser.is_open:
#             ser.close()  # Ensure the serial port is closed on exit
#             print("Serial port closed.")
#
#
# if __name__ == "__main__":
#     Read_From_Serial()
