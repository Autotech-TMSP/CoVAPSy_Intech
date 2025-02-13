#include <Wire.h>

volatile bool dataReceived = false;
volatile char receivedData[32]; // Buffer to hold received data
volatile int receivedLength = 0;

const int sensorPin_Lipo = A2; // select the input pin for the battery sensor
const int sensorPin_NiMh = A3; // select the input pin for the battery sensor

const float r1_LiPo = 560;  // resistance of the first resistor
const float r1_NiMh = 560;  // resistance of the second resistor
const float r2_LiPo = 1500; // resistance of the second resistor
const float r2_NiMh = 1000; // resistance of the second resistor
float voltage_LiPo = 0;     // variable to store the value read
float voltage_NiMh = 0;     // variable to store the value read

volatile bool dataRequested = false;

void setup()
{
    Wire.begin(8);                // Join I2C bus with address #8
    Wire.onReceive(receiveEvent); // Register receive event
    Wire.onRequest(requestEvent); // Register request event
    Serial.begin(115200);
    pinMode(sensorPin_Lipo, INPUT);
    pinMode(sensorPin_NiMh, INPUT);
}

void loop()
{
    if (dataReceived)
    {
        dataReceived = false;
        Serial.print("Received: ");
        for (int i = 0; i < receivedLength; i++)
        {
            Serial.print(receivedData[i]);
        }
        Serial.println();
    }
    // read the value from the sensor:
    voltage_LiPo = analogRead(sensorPin_Lipo);
    voltage_NiMh = analogRead(sensorPin_NiMh);
    voltage_LiPo = voltage_LiPo * (5.0 / 1023.0) * ((r1_LiPo + r2_LiPo) / r1_LiPo);
    voltage_NiMh = voltage_NiMh * (5.0 / 1023.0) * ((r1_NiMh + r2_NiMh) / r1_NiMh);
    Serial.print("Voltage LiPo: ");
    Serial.print(voltage_LiPo);
    Serial.print("V, Voltage NiMh: ");
    Serial.println(voltage_NiMh);

    delay(100);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany)
{
    receivedLength = 0;
    while (Wire.available())
    {
        receivedData[receivedLength++] = Wire.read(); // Receive byte as a character
    }
    if (receivedLength > 1)
    {
        dataReceived = true;
    }
}

// Function that executes whenever data is requested by master
void requestEvent() {
  const int numFloats = 2; // Number of floats to send
  float data[numFloats] = {voltage_LiPo, voltage_NiMh}; // Example float values to send
  byte* dataBytes = (byte*)data;

  Wire.write(dataBytes, sizeof(data));
}