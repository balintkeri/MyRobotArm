from .lowLevel import *
from .config import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    z: float

@dataclass
class Angle:
    node: int
    angle: float



class Middleware(ABC):
    def __init__(self):
        self.nodes = []
        for pin in servo_pins:
            self.nodes.append(Node(pin.id, pin.stopActuation, pin.initAngle))

    @abstractmethod
    def move_to(self, position: Position):
        pass

    def getNode(self, id: int):
        if id < 0 or id >= len(self.nodes):
            raise IndexError("Node ID out of range")
        return self.nodes[id]
    
    def cleanup(self):
        for node in self.nodes:
            node._cleanup()
        

class InverseKinematics(Middleware):
    def move_to(self, position: Position):
        denavit_hartenberg_params = [
            # (x_move, x_rotate, z_move, z_rotate)
            (0, -90, 70, "q1"), # Joint 1
            (0, 180, 40, "q2"), # Joint 2
            (180, 0, 25, "q3"), # Joint 3
        ]

        

class AngleControl(Middleware):
    def move_to(self, position: Angle):
        self.getNode(position.node).move(position.angle)