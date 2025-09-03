#include "RandomLinkGenerator.h"
#include <random>
#include <time.h> 

String generateRandomLink(int i,int ID_m) {
  // Get the current date and time
  time_t now = time(nullptr);
  struct tm *timeinfo = localtime(&now);

  // Format date and time
  char date[11]; // Format: YYYY-MM-DD (10 chars + null terminator)
  strftime(date, sizeof(date), "%Y-%m-%d", timeinfo);

  char formattedTime[20]; // Format: HH%3AMM%3ASS (to include URL-encoded separators)
  snprintf(formattedTime, sizeof(formattedTime), "%02d%%3A%02d%%3A%02d", 
           timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec);

  // Generate random values
  float left_inverter_max_temp = random(8000, 10000) / 100.0;
  float right_inverter_max_temp = random(8000, 10000) / 100.0;
  float ambient_temperature = random(2000, 4000) / 100.0;
  float car_speed_gauge = random(0, 8000) / 100.0;
  float lat = random(45000000, 46000000) / 1000000.0;
  float lon = random(-2000000, -1000000) / 1000000.0;
  float yaw_rate = random(0, 3000) / 100.0;
  float baro = random(95000, 105000) / 100.0;
  float heading_angle = random(0, 36000) / 100.0;
  String heading_dir[] = { "North", "South", "East", "West", "North-East", "South-West" };
  String heading = heading_dir[random(0, 6)];
  float left_wheel_spd = random(5000, 6000) / 100.0;
  float right_wheel_spd = random(5000, 6000) / 100.0;
  float left_mosfet_1 = random(6000, 7000) / 100.0;
  float left_mosfet_2 = random(6000, 7000) / 100.0;
  float left_mosfet_3 = random(6000, 7000) / 100.0;
  float left_motor_temp = random(7000, 8000) / 100.0;
  float right_mosfet_1 = random(8000, 9500) / 100.0;
  float right_mosfet_2 = random(8000, 9500) / 100.0;
  float right_mosfet_3 = random(8000, 9500) / 100.0;
  float right_motor_temp = random(8000, 9000) / 100.0;
  float total_voltage = random(10000, 11000) / 100.0;
  float total_current = random(400, 600) / 100.0;
  float power_consumed = random(1000, 1500) / 100.0;
  float energy_consumed = random(3000, 4000) / 100.0;
  float soc = i;
  String STATES[] = { "0", "1" };
  String turnright = STATES[random(0, 2)];
  String turnleft = STATES[random(0, 2)];
  String lights_v1 = STATES[random(0, 2)];
  String lights_v2 = STATES[random(0, 2)];

  // Create URL with actual date and time
  String url = "https://racingteam.rf.gd/new/add.php?";
  url += "ID=" + String(ID_m);
  url += "&left_inverter_max_temp=" + String(left_inverter_max_temp, 2);
  url += "&right_inverter_max_temp=" + String(right_inverter_max_temp, 2);
  url += "&ambient_temperature=" + String(ambient_temperature, 2);
  url += "&car_speed_gauge=" + String(car_speed_gauge, 2);
  url += "&lat=" + String(lat, 6);
  url += "&lon=" + String(lon, 6);
  url += "&yaw_rate=" + String(yaw_rate, 2);
  url += "&baro=" + String(baro, 2);
  url += "&heading_angle=" + String(heading_angle, 2);
  url += "&heading_dir=" + heading;
  url += "&left_wheel_spd=" + String(left_wheel_spd, 2);
  url += "&right_wheel_spd=" + String(right_wheel_spd, 2);
  url += "&left_mosfet_1=" + String(left_mosfet_1, 2);
  url += "&left_mosfet_2=" + String(left_mosfet_2, 2);
  url += "&left_mosfet_3=" + String(left_mosfet_3, 2);
  url += "&left_motor_temp=" + String(left_motor_temp, 2);
  url += "&right_mosfet_1=" + String(right_mosfet_1, 2);
  url += "&right_mosfet_2=" + String(right_mosfet_2, 2);
  url += "&right_mosfet_3=" + String(right_mosfet_3, 2);
  url += "&right_motor_temp=" + String(right_motor_temp, 2);
  url += "&total_voltage=" + String(total_voltage, 2);
  url += "&total_current=" + String(total_current, 2);
  url += "&power_consumed=" + String(power_consumed, 2);
  url += "&energy_consumed=" + String(energy_consumed, 2);
  url += "&soc=" + String(soc, 2);
  url += "&turnright=" + turnright;
  url += "&turnleft=" + turnleft;
  url += "&lights_v1=" + lights_v1;
  url += "&lights_v2=" + lights_v2;
  return url;
}
