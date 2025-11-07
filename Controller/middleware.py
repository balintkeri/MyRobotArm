from .lowLevel import *
from .config import *
from abc import ABC, abstractmethod
from dataclasses import dataclass
import threading

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
    def move_to(self, angles: list):
        commands = []
        for i, angle in enumerate(angles):
            if isinstance(angle, Angle):
                commands.append(threading.Thread(target=self.getNode(angle.node).move, args=(angle.angle,)))
            else:
                commands.append(threading.Thread(target=self.getNode(i).move, args=(angle,)))

        for command in commands:
                command.start()
        for command in commands:
            command.join() # Wait for all threads to complete