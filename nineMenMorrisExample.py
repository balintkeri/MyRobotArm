

import tkinter as tk
import threading

from Controller import RobotArm, AngleControl, InverseKinematics


class ExampleApp:
    TABLE_POSITION = {
        '000': (71, 111, 116),
        '001': (68, 93, 108),
        '002': (71, 73, 116),

        '010': (57,118,84),

        '012': (56,64,80),

        '020': (52,132,62),
        '021': (54,90,48),
        '022': (54,45,58),


        '100': (65,106,100),
        '101': (63,92,95),
        '102': (65, 77, 100),

        '110': (56,110,79),

        '112': (56,72,79),

        '120': (55,102,67),
        '121': (54,92,57),
        '122': (53,63,60),

        '200': (58,100,83),
        '201': (60,92,85),
        '202': (58,82,83),

        '210': (57,101,76),

        '212': (56,83,76),

        '220': (55,100,66),
        '221': (53,91,63),
        '222': (54,79,63),
    }


    def __init__(self, root):
        self.root = root
        self.root.title("Nine Men's Morris Example")
        self.robot_arm = RobotArm()
        self.buttons = {}

        # Coordinates for button placement (row, column) for a 7x7 grid
        positions = {
   '000': (0, 0),                               '001': (0, 3),                            '002': (0, 6),
                  '100': (1, 1),                '101': (1, 3),              '102': (1, 5),
                                 '200': (2, 2), '201': (2, 3), '202': (2, 4),   
    '010': (3, 0),'110': (3, 1), '210': (3, 2),                '212': (3, 4),'112': (3, 5),'012': (3, 6),
                                 '220': (4, 2), '221': (4, 3), '222': (4, 4),
                  '120': (5, 1),                '121': (5, 3),               '122': (5, 5),
    '020': (6, 0),                              '021': (6, 3),                             '022': (6, 6),
        }

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # exit button

        exit_button = tk.Button(self.root, text="Exit", command=self.exit)
        exit_button.pack(pady=10)

        for key, (row, col) in positions.items():
            btn = tk.Button(frame, text=key, width=4, height=2, command=lambda k=key: self.buttonPressed(k))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons[key] = btn

    def exit(self):
        self.robot_arm.cleanup()
        self.root.destroy()
        

    def buttonPressed(self, key):
        self.goBase()
        if key in self.TABLE_POSITION:
            commands = []
            for i, angle in enumerate(self.TABLE_POSITION[key]):
                commands.append( threading.Thread(target=self.robot_arm.command, kwargs={"node": i, "angle": angle}) )
            
            for command in commands:
                command.start()
            for command in commands:
                command.join()
        else:
            print(f"Position {key} not defined.")

    def goBase(self):
        commands = []
        for index, angle in enumerate([0, 90, 90]):
            commands.append( threading.Thread(target=self.robot_arm.command, kwargs={"node": index, "angle": angle}) )
        
        for command in commands:
            command.start()
        for command in commands:
            command.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExampleApp(root)
    root.mainloop()