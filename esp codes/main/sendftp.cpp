#include "SendFTP.h"
#include <string.h> // for strcpy

// timing + session state
unsigned long startTime1;
unsigned long endTime1;
bool once = true;

// NEW: track when the FTP session was opened, and a 5-min window
static unsigned long connOpenedAt = 0;
// static const unsigned long CONN_WINDOW_MS = 5UL * 60UL * 1000UL;
static const unsigned long CONN_WINDOW_MS = 1UL * 60UL * 1000UL;

SendFTP::SendFTP(const char* server,
                 const char* user,
                 const char* password,
                 const char* path,
                 const char* filename)
    : ftp(ftpServer, ftpUser, ftpPassword, 5000, 2) // pass char* refs to ESP32_FTPClient
{
    strcpy(ftpServer, server);
    strcpy(ftpUser, user);
    strcpy(ftpPassword, password);
    strcpy(ftpPath, path);
    strcpy(ftpFilename, filename);
}

void SendFTP::uploadToFTP(const String& data) {
    // now = current millis (rollover-safe when used with unsigned subtraction)
    const unsigned long now = millis();

    // Open on first use, OR refresh if the connection has lived > 5 minutes
    if (once) {
        ftp.OpenConnection();
        connOpenedAt = now;
        once = false;
    } else if ((unsigned long)(now - connOpenedAt) > CONN_WINDOW_MS) {
        // refresh the session every ~5 minutes
        ftp.CloseConnection();          // best-effort close
        ftp.OpenConnection();           // reopen
        connOpenedAt = now;             // reset age
    }

    // ~1.5 seconds
    startTime1 = millis();
    ftp.ChangeWorkDir(ftpPath);
    ftp.InitFile("Type I");
    ftp.NewFile(ftpFilename);
    ftp.Write(data.c_str());
    ftp.CloseFile();
    endTime1 = millis();
    //

    Serial.print("internal upload time: ");
    Serial.print(endTime1 - startTime1);
    Serial.println(" ms");

    // If the session just crossed 5 minutes during this upload, close now
    // so the next call starts fresh.
    if ((unsigned long)(endTime1 - connOpenedAt) >= CONN_WINDOW_MS) {
        ftp.CloseConnection();
        once = true;  // next upload will reopen
    }

    Serial.println("Uploaded JSON to FTP");
}
