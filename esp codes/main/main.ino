#include "WiFiManager.h"
#include "HTTPRequest.h"
#include "RandomLinkGenerator.h"
#include "JSONParser.h"
#include "uart.h"
#include <WiFi.h>
#include "esp_wifi.h"   // required for esp_wifi_get_phy_rate()


  const char* ssid = "Low";
  const char* password = "omega.4612";
  
  #define RXD2 16   // RX pin for Serial2
  #define TXD2 17   // TX pin for Serial2

  // const char* ssid = "A50";
  // const char* password = "23456789";

  void setup() {
    Serial.begin(115200);
    // Serial2.begin(9600);

    Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
    init_wifi(ssid, password);  // Wi-Fi initialization
    // Initialize all variables to default values
    initializeVariables();
     // open once (append=true to add to existing file)
    WiFi.setSleep(false);                 // lowers latency on uploads
    esp_wifi_set_ps(WIFI_PS_NONE);        // ensure full power, no power save


  }

  void loop() {
      receive_uart();
  }
