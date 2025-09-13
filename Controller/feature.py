
from .middleware import *


class RobotArm:
    def __init__(self):
        self.controller = AngleControl()

    def command(self, angle:float = None, node:int = None, position: Position = None):
        if self.isControlType("InverseKinematics"):
            if position is None:
                raise ValueError("Position must be provided for InverseKinematics")
            self.controller.move_to(position)
        elif self.isControlType("AngleControl"):
            if angle is None or node is None:
                raise ValueError("Angle and Node ID must be provided for AngleControl")
            self.controller.move_to(Angle(node, angle))
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
