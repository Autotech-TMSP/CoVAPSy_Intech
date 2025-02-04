#include <SPI.h>

const int SS_PIN = 10;  // Slave Select pin

void setup() {
    Serial.begin(115200);
    pinMode(SS_PIN, OUTPUT);
    digitalWrite(SS_PIN, HIGH);  // Ensure SS stays high for now

    SPI.begin();  // Initialize SPI
    SPI.setClockDivider(SPI_CLOCK_DIV128);  // Set SPI clock to 1/8th of the system clock
    SPI.setDataMode(SPI_MODE0);  // Set SPI mode to 0
    SPI.setBitOrder(MSBFIRST);  // Set bit order to MSB first
}

void loop() {
    digitalWrite(SS_PIN, LOW);  // Enable slave
    delay(10);  // Small delay to ensure slave is ready

    float voltage_LiPo = 3.0;
    float voltage_NiMh = 5.0;

    // Request data from the slave
    SPI.transfer(0x01);  // Send a dummy byte to initiate the transfer
    SPI.transfer((byte*)&voltage_LiPo, sizeof(voltage_LiPo));
    SPI.transfer((byte*)&voltage_NiMh, sizeof(voltage_NiMh));

    digitalWrite(SS_PIN, HIGH);  // Disable slave

    // Print the received voltages
    Serial.print("Voltage LiPo: ");
    Serial.print(voltage_LiPo);
    Serial.print("V, Voltage NiMh: ");
    Serial.println(voltage_NiMh);

    delay(1);  // Wait for a second before the next request
}