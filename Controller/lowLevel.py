import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Node:
    def __init__(self, id: int, autoStopActuation: bool = True, init_angle: float = 0):
        self.id = id
        self._setup()
        self.angle = init_angle
        self.autoStopActuation = autoStopActuation  

    def _setup(self):
        GPIO.setup(self.id, GPIO.OUT)
        self.pwm = GPIO.PWM(self.id, 50)
        self.pwm.start(0)

        self.set_angle(self.angle)

    def _cleanup(self):
        self.pwm.stop()
        GPIO.cleanup(self.id)

    def move(self, angle:float):
    
        step = 1 if angle > self.angle else -1
        for a in range(int(self.angle), int(angle), step):
            self.set_angle(a)
            time.sleep(0.02)
        self.set_angle(angle)
        self.angle = angle
        self.stopActuation()



    def set_angle(self, angle: float):
        duty = angle / 18 + 2
        self.pwm.ChangeDutyCycle(duty)

    def stopActuation(self):
        if self.autoStopActuation:
            time.sleep(0.3)
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

