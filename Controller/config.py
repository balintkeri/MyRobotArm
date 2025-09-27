
from dataclasses import dataclass

@dataclass
class NodeConfig:
    id: int
    stopActuation: bool = True
    initAngle: float = 0

servo_pins = [
    NodeConfig(id = 31,  initAngle=90),
    NodeConfig(id = 32, stopActuation=False,),
    NodeConfig(id = 33, initAngle=90),
]  # GPIO pins for servos
