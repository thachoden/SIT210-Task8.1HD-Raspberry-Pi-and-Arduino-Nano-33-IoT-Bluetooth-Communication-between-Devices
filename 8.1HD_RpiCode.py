from bluepy import btle
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
RED_PIN = 22
GREEN_PIN = 27
BLUE_PIN = 17

# Set up the GPIO pins as outputs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def off_all_led():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
def handle_led(distance):
    if distance < 5:
        off_all_led()
        GPIO.output(RED_PIN, GPIO.HIGH)
    elif distance >= 5 and distance <10:
        off_all_led()
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.HIGH)
    elif distance >=10 and distance < 15:
        off_all_led()
        GPIO.output(GREEN_PIN, GPIO.HIGH)
    else:
        off_all_led()
def main():
    target_device = "ec:62:60:81:3c:da"
    # Connect to device
    peripheral = btle.Peripheral(target_device)
    # Get service and characteristic UUIDs
    service_uuid = btle.UUID("12345678-1234-5678-1234-56789abcdef0")
    char_uuid = btle.UUID("abcdef01-1234-5678-1234-56789abcdef0")

    service = peripheral.getServiceByUUID(service_uuid)
    characteristic = service.getCharacteristics(char_uuid)[0]

    try:
        while True:
            try:
                # Write data to characteristic
                message = "Data request"
                characteristic.write(message.encode('utf-8'), withResponse=True)
                data = characteristic.read()
                distance = int(data.decode('utf-8'))
                handle_led(distance)
            except btle.BTLEDisconnectError:
                print("Device disconnected. Attempting to reconnect...")
                peripheral.disconnect()  # Disconnect if not already done
                peripheral = btle.Peripheral(target_device)
                service = peripheral.getServiceByUUID(service_uuid)
                characteristic = service.getCharacteristics(char_uuid)[0]
    except KeyboardInterrupt:
        print("")
        GPIO.cleanup()
        peripheral.disconnect()

if __name__ == "__main__":
        main()
