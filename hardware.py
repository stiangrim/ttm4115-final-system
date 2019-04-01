import RPi.GPIO as GPIO

BUTTON_PIN = 7
BUTTON_PRESSED = false


def GPIO_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=my_callback, bouncetime=300)


def my_callback(channel):
    print("This is an edge event callback function")
    BUTTON_PRESSED = not BUTTON_PRESSED


def GPIO_cleanup():
    GPIO.cleanup()

