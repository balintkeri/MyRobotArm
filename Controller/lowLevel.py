import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Node:
    def __init__(self, id: int):
        self.id = id
        self._setup()

    def _setup(self):
        GPIO.setup(self.id, GPIO.OUT)
        self.pwm = GPIO.PWM(self.id, 50)
        self.pwm.start(0)

    def _cleanup(self):
        self.pwm.stop()
        GPIO.cleanup(self.id)

    def set_angle(self, angle: float):
        duty = angle / 18 + 2
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)


class CurrentSensor:
    def __init__(self, id: int):
        self.id = id
        self._setup()

    def _setup(self):
        GPIO.setup(self.id, GPIO.IN)

    def read_value(self) -> int:
        return GPIO.input(self.id)

    def _cleanup(self):
        GPIO.cleanup(self.id)

