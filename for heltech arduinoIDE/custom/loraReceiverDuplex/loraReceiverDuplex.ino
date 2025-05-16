/*
  LoRa Demo 3
  lora-demo3.ino
  Bi-directional LED control (duplex communications)
  Requires LoRa Library by Sandeep Mistry - https://github.com/sandeepmistry/arduino-LoRa
  sendMessage & onReceive functions based upon "LoRaDuplexCallback" code sample by Tom Igoe

  DroneBot Workshop 2023
  https://dronebotworkshop.com
*/

// Include required libraries
#include <SPI.h>
#include <LoRa.h>

// Define the pins used by the LoRa module
// const int csPin = 4;     // LoRa radio chip select
// const int resetPin = 2;  // LoRa radio reset
// const int irqPin = 3;    // Must be a hardware interrupt pin

// LED connection
const int ledPin = 9;

// Outgoing message variable
String outMessage;

// Message counter
byte msgCount = 0;

// Receive message variables
String contents = "";
String toCompareTo = "led on";
bool rcvButtonState;

// Source and destination addresses
byte localAddress = 0xCC;  // address of this device
byte destination = 0xBB;   // destination to send to where 0xFF is globa broadcast 

// Pushbutton variables
// int buttonPin = 8;
// int sendButtonState;

void setup() {

  // Set pushbutton as input
//  pinMode(buttonPin, INPUT_PULLUP);

  // Set LED as output


  Serial.begin(9600);
  while (!Serial)
    ;

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  Serial.println("set to high");
  delay(500);
  digitalWrite(ledPin, LOW);
  Serial.println("set to low");

  Serial.println("LoRa Duplex with callback");

  // Setup LoRa module
  //LoRa.setPins(csPin, resetPin, irqPin);

  // Start LoRa module at local frequency
  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1)
      ;
  }

  // Set Receive Call-back function
  LoRa.onReceive(onReceive);

  // Place LoRa in Receive Mode
  LoRa.receive();

  Serial.println("LoRa init succeeded.");
}

void loop() {

  // Get pushbutton state
  //sendButtonState = digitalRead(buttonPin);

  // Send packet if button pressed
  // if (sendButtonState == LOW) {

    // Compose and send message
    outMessage = toCompareTo;
    // sendMessage(outMessage);
    // delay(500);

    // Place LoRa back into Receive Mode
    LoRa.receive();
    // delay(2000);
  // }
}

// Send LoRa Packet
void sendMessage(String outgoing) {
  LoRa.beginPacket();             // start packet
  LoRa.write(destination);        // add destination address
  LoRa.write(localAddress);       // add sender address
  LoRa.write(msgCount);           // add message ID
  LoRa.write(outgoing.length());  // add payload length
  LoRa.print(outgoing);           // add payload
  LoRa.endPacket();               // finish packet and send it
  msgCount++;                     // increment message ID
}

// Receive Callback Function
void onReceive(int packetSize) {
  if (packetSize == 0) return;  // if there's no packet, return

  // Read packet header bytes:
  int recipient = LoRa.read();        // recipient address
  byte sender = LoRa.read();          // sender address
  byte incomingMsgId = LoRa.read();   // incoming msg ID
  byte incomingLength = LoRa.read();  // incoming msg length

  String incoming = "";  // payload of packet

  while (LoRa.available()) {        // can't use readString() in callback, so
    incoming += (char)LoRa.read();  // add bytes one by one
  }

  if (incomingLength != incoming.length()) {  // check length for error
    Serial.println("error: message length does not match length");
    return;  // skip rest of function
  }

  // If the recipient isn't this device or broadcast,
  if (recipient != localAddress && recipient != 0xFF) {
    Serial.println("This message is not for me.");
    return;  // skip rest of function
  }

  // If message is for this device, or broadcast, print details:
  Serial.println("Received from: 0x" + String(sender, HEX));
  Serial.println("Sent to: 0x" + String(recipient, HEX));
  Serial.println("Message ID: " + String(incomingMsgId));
  Serial.println("Message length: " + String(incomingLength));
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + String(LoRa.packetRssi()));
  Serial.println("Snr: " + String(LoRa.packetSnr()));
  Serial.println();


  // process msg
  if (incoming.equals(toCompareTo)) {
    digitalWrite(ledPin, HIGH);
    Serial.println("led on");
    delay(500);
    digitalWrite(ledPin, LOW);
    Serial.println("led off");
  }

}