


from Controller import RobotArm


class RobotArmAdapter:
    def __init__(self):
        self.robotArm = RobotArm()
        self.TABLE_POSITION = {
        'safestate': [0, 90, 90],
        '000': [71, 111, 116],
        '001': [68, 93, 108],
        '002': [71, 73, 116],

        '010': [57,118,84],

        '012': [56,64,80],

        '020': [52,132,62],
        '021': [54,90,48],
        '022': [54,45,58],


        '100': [65,106,100],
        '101': [63,92,95],
        '102': [65, 77, 100],

        '110': [56,110,79],

        '112': [56,72,79],

        '120': [55,102,67],
        '121': [54,92,57],
        '122': [53,63,60],

        '200': [58,100,83],
        '201': [60,92,85],
        '202': [58,82,83],

        '210': [57,101,76],

        '212': [56,83,76],

        '220': [55,100,66],
        '221': [53,91,63],
        '222': [54,79,63],
    }
        
    def move(self, start, end):
        self.robotArm.command(angles=self.TABLE_POSITION[start])
        self.robotArm.MagnetOn()
        self.robotArm.command(angles=self.TABLE_POSITION['safestate'])
        self.robotArm.command(angles=self.TABLE_POSITION[end])
        self.robotArm.MagnetOff()
        self.robotArm.command(angles=self.TABLE_POSITION['safestate'])