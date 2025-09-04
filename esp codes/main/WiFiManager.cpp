#include "WiFiManager.h"

void init_wifi(const char* ssid, const char* password) {
  Serial.print("[WiFi] Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  int tryDelay = 500;
  int numberOfTries = 20;

  while (WiFi.status() != WL_CONNECTED && numberOfTries > 0) {
    delay(tryDelay);
    numberOfTries--;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("[WiFi] WiFi is connected!");
    Serial.print("[WiFi] IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("[WiFi] Failed to connect.");
  }
}

void disconnect_from_wifi() {
  Serial.println("[WiFi] Disconnecting from WiFi!");
  WiFi.disconnect();
  delay(1000);
}
