import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Node:
    def __init__(self, id: int):
        self.id = id
        self._setup()
        self.angle = None

    def _setup(self):
        GPIO.setup(self.id, GPIO.OUT)
        self.pwm = GPIO.PWM(self.id, 50)
        self.pwm.start(0)

    def _cleanup(self):
        self.pwm.stop()
        GPIO.cleanup(self.id)


    def initAngle(self, angle: float):
        if self.angle is None:
            self.set_angle(angle)
            self.angle = angle
            self.stopActuation()
            return True
        else:
            return False

    def move(self, angle:float):
        if self.initAngle(angle):
            return
        
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

