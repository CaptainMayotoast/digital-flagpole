import RPi.GPIO as GPIO
import time

RED_LED_PIN = 10
BLUE_LED_PIN = 27
RED_BUTTON_PIN = 24
BLUE_BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
GPIO.setup(RED_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BLUE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Blinking LED. Press Ctrl+C to quit")

try:
    while True:
        GPIO.output(RED_LED_PIN, GPIO.HIGH)
        if GPIO.input(BLUE_BUTTON_PIN, GPIO.LOW):
            GPIO.output(BLUE_LED_PIN, GPIO.LOW)
        time.sleep(5e-2)
        GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
        if GPIO.input(RED_BUTTON_PIN, GPIO.LOW):
            GPIO.output(RED_LED_PIN, GPIO.LOW)
        time.sleep(5e-2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()