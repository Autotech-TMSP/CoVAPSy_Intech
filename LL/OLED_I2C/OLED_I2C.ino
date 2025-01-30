#include <Wire.h>
#include <U8glib.h> // for use with a TF051

#define WIRE Wire
String message = "Hello, World!";

// Initialize the display
U8GLIB_SSD1306_128X64 display(U8G_I2C_OPT_NONE);

void setup() {
  WIRE.begin();

  Serial.begin(115200);
  while (!Serial)
     delay(10);
  Serial.println("\nI2C Scanner");

  // Check if the display is connected
  WIRE.beginTransmission(0x3C); // Replace with the correct I2C address found
  if (WIRE.endTransmission() == 0) {
    Serial.println("OLED display found at address 0x3C");
  } else {
    Serial.println("OLED display not found at address 0x3C");
    while (1); // Stop execution if display is not found
  }

  // Display initialization
  display.setFont(u8g_font_unifont);
}

void loop() {
  // Draw the message on the display
  display.firstPage();
  do {
    display.drawStr(0, 22, message.c_str());
  } while (display.nextPage());

  delay(1000);
}