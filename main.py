


from .Controller import RobotArm


class RobotArmAdapter:
    def __init__(self):
        self.robotArm = RobotArm()
        self.positions = {
        'safestate': [0, 90, 90],
        0: [71, 111, 116],
        1: [68, 93, 108],
        2: [71, 73, 116],

        3: [57,118,84],

        4: [56,64,80],

        5: [52,132,62],
        6: [54,90,48],
        7: [54,45,58],


        8: [65,106,100],
        9: [63,92,95],
        10: [65, 77, 100],

        11: [56,110,79],

        12: [56,72,79],

        13: [55,102,67],
        14: [54,92,57],
        15: [53,63,60],
        16: [58,100,83],
        17: [60,92,85],
        18: [58,82,83],

        19: [57,101,76],

        20: [56,83,76],
        21: [55,100,66],
        22: [53,91,63],
        23: [54,79,63],
        
        'takeoff': [57,120,76],
        'dropoff': [58,60,83]
        }
        
    def move(self, positions):
        start = positions[0]
        end = positions[1]
        self.robotArm.command(angles=self.positions[start])
        self.robotArm.MagnetOn()
        self.robotArm.command(angles=self.positions['safestate'])
        self.robotArm.command(angles=self.positions[end])
        self.robotArm.MagnetOff()
        self.robotArm.command(angles=self.positions['safestate'])