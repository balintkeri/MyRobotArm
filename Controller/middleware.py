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
        raise NotImplementedError("Inverse Kinematics not implemented yet")

        

class AngleControl(Middleware):
    def move_to(self, angles: list[Angle]):
        for angle in angles:
            self.getNode(angle.node).move(angle.angle)