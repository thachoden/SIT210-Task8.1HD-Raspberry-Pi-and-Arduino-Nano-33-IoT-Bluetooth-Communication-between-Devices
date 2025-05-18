from bluepy import btle
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
RED_PIN = 22

# Set up the GPIO pins as outputs
GPIO.setup(RED_PIN, GPIO.OUT)

# Set up PWM for each LED
led_pwm = GPIO.PWM(RED_PIN, 100)   # 100 Hz
led_pwm.start(0)   # Start with 0% duty cycle
def off_led():
    led_pwm.ChangeDutyCycle(0)
def handle_led(distance):
    if distance < 0.5:
        led_pwm.ChangeDutyCycle(100)  # 0.5 cm
    elif distance < 1.0:
        led_pwm.ChangeDutyCycle(95)    # 1.0 cm
    elif distance < 1.5:
        led_pwm.ChangeDutyCycle(90)    # 1.5 cm
    elif distance < 2.0:
        led_pwm.ChangeDutyCycle(85)    # 2.0 cm
    elif distance < 2.5:
        led_pwm.ChangeDutyCycle(80)    # 2.5 cm
    elif distance < 3.0:
        led_pwm.ChangeDutyCycle(75)    # 3.0 cm
    elif distance < 3.5:
        led_pwm.ChangeDutyCycle(70)    # 3.5 cm
    elif distance < 4.0:
        led_pwm.ChangeDutyCycle(65)    # 4.0 cm
    elif distance < 4.5:
        led_pwm.ChangeDutyCycle(60)    # 4.5 cm
    elif distance < 5.0:
        led_pwm.ChangeDutyCycle(55)    # 5.0 cm
    elif distance < 5.5:
        led_pwm.ChangeDutyCycle(50)
    elif distance < 6.0:
        led_pwm.ChangeDutyCycle(45)
    elif distance < 6.5:
        led_pwm.ChangeDutyCycle(40)
    elif distance < 7.0:
        led_pwm.ChangeDutyCycle(35)
    elif distance < 7.5:
        led_pwm.ChangeDutyCycle(30)
    elif distance < 8.0:
        led_pwm.ChangeDutyCycle(25)
    elif distance < 8.5:
        led_pwm.ChangeDutyCycle(20)
    elif distance < 9.0:
        led_pwm.ChangeDutyCycle(15)
    elif distance < 9.5:
        led_pwm.ChangeDutyCycle(10)
    elif distance < 10.0:
        led_pwm.ChangeDutyCycle(5)
    else:
        off_led()  

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
    try:
        main()
    except Exception as e:
        print(f"{e}")
        GPIO.cleanup()
