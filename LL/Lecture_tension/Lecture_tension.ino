#include <SPI.h>
#include <avr/io.h>

const int SCK_PIN = 13;  // D13 = pin19 = PortB.5
const int MISO_PIN = 12;  // D12 = pin18 = PortB.4
const int MOSI_PIN = 11;  // D11 = pin17 = PortB.3
const int SS_PIN = 10;    // D10 = pin16 = PortB.2
const int sensorPin_Lipo = A2;   // select the input pin for the battery sensor
const int sensorPin_NiMh = A3;   // select the input pin for the battery sensor

const float r1_LiPo = 560;         // resistance of the first resistor
const float r1_NiMh = 560;       // resistance of the second resistor
const float r2_LiPo = 1500;       // resistance of the second resistor
const float r2_NiMh = 1000;     // resistance of the second resistor
float voltage_LiPo = 0;   // variable to store the value read
float voltage_NiMh = 0;   // variable to store the value read

volatile bool dataRequested = false;

void setup() {
    Serial.begin(115200);
    pinMode(MISO_PIN, OUTPUT);
    pinMode(SS_PIN, INPUT_PULLUP);
    SPI.begin();
    SPCR |= _BV(SPE); // Enable SPI as slave
    SPI.attachInterrupt(); // Enable SPI interrupt
}

ISR(SPI_STC_vect) {
    dataRequested = true;
}

void loop() {
    // read the value from the sensor:
    voltage_LiPo = analogRead(sensorPin_Lipo);
    voltage_NiMh = analogRead(sensorPin_NiMh);
    voltage_LiPo = voltage_LiPo * (5.0 / 1023.0) * ((r1_LiPo + r2_LiPo) / r1_LiPo);
    voltage_NiMh = voltage_NiMh * (5.0 / 1023.0) * ((r1_NiMh + r2_NiMh) / r1_NiMh);
    Serial.print("Voltage LiPo: ");
    Serial.print(voltage_LiPo);
    Serial.print("V, Voltage NiMh: ");
    Serial.println(voltage_NiMh);

    if (dataRequested) {
        dataRequested = false;
        // Send the voltage values over SPI
        SPI.transfer((byte*)&voltage_LiPo, sizeof(voltage_LiPo));
        SPI.transfer((byte*)&voltage_NiMh, sizeof(voltage_NiMh));
    }

    delay(100);
}