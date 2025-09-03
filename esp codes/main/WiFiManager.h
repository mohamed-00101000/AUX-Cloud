#ifndef WIFIMANAGER_H
#define WIFIMANAGER_H

#include <WiFi.h>

void init_wifi(const char* ssid, const char* password);
void disconnect_from_wifi();

#endif
