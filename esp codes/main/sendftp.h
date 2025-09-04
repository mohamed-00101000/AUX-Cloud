#ifndef SENDFTP_H
#define SENDFTP_H

#include <Arduino.h>
#include <WiFi.h>
#include <ESP32_FTPClient.h>

class SendFTP {
private:
    char ftpServer[64];
    char ftpUser[64];
    char ftpPassword[64];
    char ftpPath[128];
    char ftpFilename[64];
    ESP32_FTPClient ftp;

public:
    SendFTP(const char* server,
            const char* user,
            const char* password,
            const char* path,
            const char* filename);

    void uploadToFTP(const String& data);
};

#endif
