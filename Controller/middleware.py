from .lowLevel import *
from .config import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    z: float

class Angle:
    node: int
    angle: float

class Middleware(ABC):
    def __init__(self):
        self.nodes = []
        for pin in servo_pins:
            self.nodes.append(Node(pin))

    @abstractmethod
    def move_to(self, position: Position):
        pass

    def getNodes(self, id: int):
        if id < 0 or id >= len(self.nodes):
            raise IndexError("Node ID out of range")
        return self.nodes[id]

class InverseKinematics(Middleware):
    def move_to(self, position: Position):
        pass #TODO

class AngleControl(Middleware):
    def move_to(self, position: Angle):
        self.getNodes(position.node).set_angle(position.angle)