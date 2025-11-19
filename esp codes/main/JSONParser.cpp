#include "JSONParser.h"
#include "HTTPRequest.h"
#include <ArduinoJson.h>
#include <sstream>
#include <iostream>
#include "SendFTP.h"
unsigned long startTime;
unsigned long endTime;
void get_data(const String& url) {
  fetchdatafromjson(url);
}

// Global variables
std::map<int, String> variableValues;
int id_mm=0;
String jsonData;
SendFTP ftpSender(
    "ftpupload.net",
    "if0_38887836",
    "uZnrqJ55D3nN",
    "/htdocs/new",
    "data.json"
);

// Default values for all IDs
const String defaultValues[TOTAL_VARIABLES] = {
    "91.10", "86.61", "34.31", "36.55", "45.426567", "-1.580406", "7.34", "1038.23",
    "208.84", "West", "58.18", "57.36", "65.15", "68.49", "67.65", "75.45",
    "91.09", "84.41", "91.34", "82.72", "105.12", "4.34", "13.92", "35.69",
    "81.90", "1", "1", "1"
};
const String variableNames[TOTAL_VARIABLES] = {
        "left_inverter_max_temp", "right_inverter_max_temp", "ambient_temperature", "car_speed_gauge",
        "lat", "lon", "yaw_rate", "baro", "heading_angle", "heading_dir", "left_wheel_spd",
        "right_wheel_spd", "left_mosfet_1", "left_mosfet_2", "left_mosfet_3", "left_motor_temp",
        "right_mosfet_1", "right_mosfet_2", "right_mosfet_3", "right_motor_temp", "total_voltage",
        "total_current", "power_consumed", "energy_consumed", "soc", "turnright", "turnleft", "lights_v1"
};


// Initialize variables to default values
void initializeVariables() {
    for (int i = 1; i <= TOTAL_VARIABLES; i++) {
        variableValues[i] = defaultValues[i - 1];
    }
}

// Parse the frame and update variable values
void parseFrame(const String& buffer) {
    // Record the start time
  
    int pos = 0;

    while (pos != -1) {
        int next = buffer.indexOf(',', pos);
        String pair = (next == -1) ? buffer.substring(pos) : buffer.substring(pos, next);

        int colonPos = pair.indexOf(':');
        if (colonPos != -1) {
            String idStr = pair.substring(0, colonPos);
            String value = pair.substring(colonPos + 1);

            if (idStr.startsWith("ID_")) {
                int id = idStr.substring(3).toInt();
                if (id >= 1 && id <= TOTAL_VARIABLES) {
                    variableValues[id] = value;
                }
            }
        }
        pos = (next == -1) ? -1 : next + 1;
    }
    jsonData = mapValues();
    // Serial.println(jsonData);
    startTime = millis();
    ftpSender.uploadToFTP(jsonData);
  
    // Record the end time
    endTime = millis();
    // Print the elapsed time
  Serial.print("Upload time: ");
  Serial.print(endTime - startTime);
  Serial.println(" ms");
}
String mapValues(){
    std::stringstream result;
    result << "[\n{\n ";

    for(int i = 0; i < TOTAL_VARIABLES; i++){
        if (strcmp(variableNames[i].c_str(), "heading_dir") == 0) {
            // Wrap heading_dir value in quotes
            result << '"' << variableNames[i].c_str() << '"' << " : \"" << variableValues[i + 1].c_str()<<'"';
        } else {
            result << '"' << variableNames[i].c_str() << '"' << " : " << variableValues[i + 1].c_str();
        }

        if (i < TOTAL_VARIABLES - 1){
            result << ",\n ";
        }
    }
    result << "\n}\n]";
    return String(result.str().c_str()); // Convert std::string to Arduino String
}


// Generate the full URL with current variable values
String generateURL() {
    String url = "https://racingteam.rf.gd/new/add.php?";

   url += "ID=" + String(id_mm);
    for (int i = 0; i < TOTAL_VARIABLES; i++) {
        url += "&" + variableNames[i] + "=" + variableValues[i + 1];
    }
   id_mm++;

    return url;
}
