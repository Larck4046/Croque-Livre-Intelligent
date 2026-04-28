from gpiozero import LED, Button
from time import sleep

class Main():
    def __init__(self, porte):
        self.relay = LED(porte)

    def open(self):
        self.relay.on()
        sleep(0.3)
        self.relay.off()


class Led():
    def __init__(self, v, r, porte_sensor):
        self.v = LED(v)
        self.r = LED(r)
        self.porte_sensor = Button(porte_sensor)

    def auto_led(self):
        while True:
            sleep(0.1)
            if self.porte_sensor.is_pressed:
                self.v.on()
                self.r.off()
            else:
                self.v.off()
                self.r.on()


if __name__ == "__main__":
    run = Led(6, 12, 13)
    run.auto_led()