#include <Wire.h>

volatile bool dataReceived = false;
volatile char receivedData[32]; // Buffer to hold received data
volatile int receivedLength = 0;

void setup() {
  Wire.begin(8); // Join I2C bus with address #8
  Wire.onReceive(receiveEvent); // Register receive event
  Wire.onRequest(requestEvent); // Register request event
  Serial.begin(9600); // Start serial communication at 9600 bps
}

void loop() {
  if (dataReceived) {
    dataReceived = false;
    Serial.print("Received: ");
    for (int i = 0; i < receivedLength; i++) {
      Serial.print(receivedData[i]);
    }
    Serial.println();
  }
  delay(100);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  receivedLength = 0;
  while (Wire.available()) {
    receivedData[receivedLength++] = Wire.read(); // Receive byte as a character
  }
  dataReceived = true;
}

// Function that executes whenever data is requested by master
void requestEvent() {
  const char* response = "Hello Master!";
  Wire.write(response);
}