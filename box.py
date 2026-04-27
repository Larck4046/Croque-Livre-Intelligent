"""

Ici sera le fichier box.py pour la gestion du boitier (commande rasberry pi et tout ce qui va avec)

porte = relay
porte ouvert seulement 0.5 seconde max

"""
from gpiozero import LED, Button
from time import sleep

class Main():
    def __init__(self, porte):
        self.porte = LED(porte) # Simplement pouvoir envoyer du courant ou non dans le RELAY
        
    def porte(self):
        self.porte.on()
        sleep(0.3)
        self.porte.off()


class Led():
    def __init__(auto, v, r,porte_sensor):
        auto.v = LED(v)
        auto.r = LED(r)
        auto.porte_sensor = Button(porte_sensor)
    def auto_led(auto):
        while True:    
            sleep(0.1)
            if auto.porte_sensor.is_pressd:
                auto.v.on()
                auto.r.off()
            else:
                auto.v.off()
                auto.r.on()

if __name__ == "__main__":
    Run = Led("v pin", "r pin", "sensor pin")
    Run.auto_led()