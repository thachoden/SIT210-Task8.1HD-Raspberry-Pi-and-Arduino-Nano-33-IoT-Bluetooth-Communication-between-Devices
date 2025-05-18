#include <ArduinoBLE.h>

const int trigPin = 2;  // Trigger pin
const int echoPin = 3; // Echo pin

BLEService customService("12345678-1234-5678-1234-56789abcdef0"); // Custom service UUID
BLECharacteristic customCharacteristic("abcdef01-1234-5678-1234-56789abcdef0", BLERead | BLEWrite | BLENotify, 20);

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("Nano33IoT");
  BLE.setAdvertisedService(customService);

  customService.addCharacteristic(customCharacteristic);
  BLE.addService(customService);
  
  BLE.advertise();
  Serial.println("BLE Peripheral device is now advertising...");
}

int getDistance() {
  long duration;
  int distance;

  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Send a 10 microsecond pulse to trigger the sensor
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance (speed of sound is 34300 cm/s)
  distance = duration * 0.034 / 2;

  return distance;
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      int distance = getDistance();
      if (customCharacteristic.written()) { 
        String data = String(distance);
        customCharacteristic.writeValue(data.c_str());
        Serial.println("Data sent");
      }
    }
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
    Serial.println("BLE Peripheral device is now advertising...");
  }
}
