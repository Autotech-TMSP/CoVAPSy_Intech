#include <SPI.h>

volatile bool dataReceived = false;
volatile byte receivedData[8];  // Buffer to hold received data
volatile byte index = 0;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);

  // Set MISO as output
  pinMode(MISO, OUTPUT);

  // Enable SPI as slave
  SPCR |= _BV(SPE);

  // Attach interrupt to SPI
  SPI.attachInterrupt();
}

ISR(SPI_STC_vect) {
  receivedData[index++] = SPDR;  // Read received byte and store in buffer
  if (index >= 8) {  // Check if we have received 8 bytes (2 floats)
    dataReceived = true;
    index = 0;
  }
}

void loop() {
  if (dataReceived) {
    dataReceived = false;

    // Convert received bytes to floats
    float received1, received2;
    memcpy(&received1, receivedData, sizeof(received1));
    memcpy(&received2, receivedData + sizeof(received1), sizeof(received2));

    // Display received data on Serial Monitor
    Serial.print("Received float 1: ");
    Serial.println(received1);
    Serial.print("Received float 2: ");
    Serial.println(received2);
  }
}