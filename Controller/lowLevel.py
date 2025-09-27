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

    def set_angle(self, angle: float):

        if angle == self.angle:
            return

        def step(tempAngle):
            duty = tempAngle / 18 + 2
            self.pwm.ChangeDutyCycle(duty)
            time.sleep(0.02 )
        
        if angle > self.angle:
            for tempAngle in range(int(self.angle), int(angle)+1):
                step(tempAngle)
        else:
            for tempAngle in range(int(self.angle), int(angle)-1, -1):
                step(tempAngle)
            
        #duty = angle / 18 + 2
        #self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)

        self.angle = angle

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

