import RPi.GPIO as GPIO
import pyttsx3

BUTTON_PIN = 7
LED_PIN = 4
DOOR_LOCKED = False


def GPIO_setup(method_to_run):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=lambda x: my_callback(method_to_run), bouncetime=300)


def GPIO_cleanup():
    GPIO.cleanup()


def my_callback(method_to_run):
    print("Button pressed!")
    global DOOR_LOCKED
    DOOR_LOCKED = not DOOR_LOCKED
    method_to_run()
    GPIO.output(LED_PIN, DOOR_LOCKED)
