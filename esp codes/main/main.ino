#include "WiFiManager.h"
#include "HTTPRequest.h"
#include "RandomLinkGenerator.h"
#include "JSONParser.h"
#include "uart.h"
#include <WiFi.h>
#include "esp_wifi.h"   // required for esp_wifi_get_phy_rate()


  const char* ssid = "Low";
  const char* password = "omega.4612";

  // const char* ssid = "A50";
  // const char* password = "23456789";

  int ID_m=0;


  String getdatafrompcurl = "https://racingteam.rf.gd/new/get.json";
  int receivedChar;
  int btnGPIO = 0;

  void setup() {
    Serial.begin(9600);
    pinMode(btnGPIO, INPUT);  
    init_wifi(ssid, password);  // Wi-Fi initialization

    // Initialize all variables to default values
    initializeVariables();
     // open once (append=true to add to existing file)
    WiFi.setSleep(false);                 // lowers latency on uploads
    esp_wifi_set_ps(WIFI_PS_NONE);        // ensure full power, no power save


  }

  int counter=0;

  void loop() {
      receive_uart();
  }
