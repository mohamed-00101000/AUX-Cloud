#ifndef JSONPARSER_H
#define JSONPARSER_H

#include <Arduino.h>

#include <string>
#include <map>

// Constants
#define TOTAL_VARIABLES 28

// Default values for all variables
extern const String defaultValues[TOTAL_VARIABLES];

// Structure to hold the latest variable values
extern std::map<int, String> variableValues;
// Function prototypes
void initializeVariables();
void parseFrame(const String& buffer);
String generateURL();
// ==== Function to Build JSON ====
String buildJson();
String mapValues();
void get_data(const  String& url);
void parseBuffer(char *Receiveddata);

#endif
