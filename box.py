"""

Ici sera le fichier box.py pour la gestion du boitier (commande rasberry pi et tout ce qui va avec)

"""
import RPi.GPIO as GPIO
import time
porte_pin=['x','x']
g_pin = 'x'
r_pin = 'x'
class Box():
    def __init__(self):
        self.p_pin = porte_pin[0]
        self.pd_pin = porte_pin[1]
        self.g_pin = g_pin
        self.r_pin = r_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.p_pin, GPIO.OUT)
        GPIO.setup(self.pd_pin, GPIO.IN)
        GPIO.setup(self.g_pin, GPIO.OUT)
        GPIO.setup(self.r_pin, GPIO.OUT)

    def open_box(self):
        GPIO.output(self.p_pin, GPIO.HIGH)
        led_state(True)
        time.sleep(0.1)
        GPIO.output(self.p_pin, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.p_pin, GPIO.HIGH)
        led_state(False)

    def led_state(self, bool(state)):
        if state:
            GPIO.output(self.g_pin, GPIO.HIGH)
            GPIO.output(self.r_pin, GPIO.LOW)
        else:
            GPIO.output(self.g_pin, GPIO.LOW)
            GPIO.output(self.r_pin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()

