
from .middleware import *


class RobotArm:
    def __init__(self):
        self.controller = AngleControl()
        self.magnet = Magnet(magnet_pin)

    def magnetOn(self):
        self.magnet.on()

    def magnetOff(self):
        self.magnet.off()

    def command(self, angles:list = None, node:int = None, position: Position = None):
        if self.isControlType("InverseKinematics"):
            if position is None:
                raise ValueError("Position must be provided for InverseKinematics")
            self.controller.move_to(position)
        elif self.isControlType("AngleControl"):
            if angles is None:
                raise ValueError("Angles must be provided for AngleControl")
            self.controller.move_to(angles)
        else:
            raise ValueError("Unknown controller type")

    def isControlType(self, controller_type):
        return self.controller.__class__.__name__ == controller_type

    def changeController(self, controller_type):
        self.controller.cleanup()
        if controller_type == "AngleControl":
            self.controller = AngleControl()
        elif controller_type == "InverseKinematics":
            self.controller = InverseKinematics()
        else:
            raise ValueError("Unknown controller type")
        
    def cleanup(self):
        self.controller.cleanup()
        self.magnet.cleanup()
