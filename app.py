
import tkinter as tk

from Controller import RobotArm, AngleControl, InverseKinematics

import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Arm Control")

        self.robot_arm = RobotArm()

        self.selectControllerFrame = tk.Frame(root)
        self.selectControllerFrame.pack(pady=10)
        self.angleControlButton = tk.Button(self.selectControllerFrame, text="Angle Control", command=self.setAngleControl)
        self.angleControlButton.pack(side=tk.LEFT, padx=5)
        self.inverseKinematicsButton = tk.Button(self.selectControllerFrame, text="Inverse Kinematics", command=self.setInverseKinematics)
        self.inverseKinematicsButton.pack(side=tk.LEFT, padx=5)

        self.controlFrame = tk.Frame(root)
        self.controlFrame.pack(pady=10)

        self.anglegridFrame = tk.Frame(self.controlFrame)
        self.anglegridFrame.pack()

        self.nodeLabel = tk.Label(self.anglegridFrame, text="Node ID")
        self.nodeLabel.grid(row=0, column=0, padx=5, pady=5)
        self.angleLabel = tk.Label(self.anglegridFrame, text="Angle (degrees)")
        self.angleLabel.grid(row=0, column=1, padx=5, pady=5)


        self.angleEntries = []
        for i in self.robot_arm.controller.nodes:
            
            node_id = i.id
            node_entry = tk.Label(self.anglegridFrame, width=10, text=str(node_id))
            node_entry.grid(row=node_id, column=0, padx=5, pady=5)
            angle_entry = tk.Scale(self.anglegridFrame, from_=0, to=180, orient=tk.HORIZONTAL, command=self.sendCommand, )
            angle_entry.set(i.angle)
            angle_entry.grid(row=node_id, column=1, padx=5, pady=5)
            self.angleEntries.append(angle_entry)


        self.exitButton = tk.Button(root, text="Exit", command=self.cleanup)
        self.exitButton.pack(pady=10)


        self.updateControlVisibility()

    def cleanup(self):
        self.robot_arm.cleanup()
        self.root.destroy()


    def updateControlVisibility(self):
        if self.robot_arm.isControlType("AngleControl"):
            self.anglegridFrame.pack()
            if hasattr(self, 'positionEntry'):
                self.positionEntry.pack_forget()
        else:
            self.anglegridFrame.pack_forget()
            if not hasattr(self, 'positionEntry'):
                self.positionEntry = tk.Entry(self.controlFrame, width=30)
                self.positionEntry.insert(0, "x,y,z")
                self.positionEntry.pack(pady=5)

    def setAngleControl(self):
        self.robot_arm.changeController("AngleControl")
        self.updateControlVisibility()
        print("Switched to Angle Control")

    def setInverseKinematics(self):
        self.robot_arm.changeController("InverseKinematics")
        self.updateControlVisibility()
        print("Switched to Inverse Kinematics")

    def sendCommand(self, _):
        commands = []
        try:
            if self.robot_arm.isControlType("AngleControl"):
                for node_id, entry in enumerate(self.angleEntries):
                    angle_str = entry.get()
                    if angle_str:
                        angle = float(angle_str)
                        commands.append(threading.Thread(target=self.robot_arm.command, args=(angle, node_id)))
                        #self.robot_arm.command(angle=angle, node=node_id)
                        print(f"Sent Angle Control Command: Node {node_id}, Angle {angle}")
            else:
                position_str = self.positionEntry.get()
                x, y, z = map(float, position_str.split(','))
                commands.append(threading.Thread(target=self.robot_arm.command, args=(None, None, self.robot_arm.controller.Position(x, y, z))))
                #self.robot_arm.command(position=self.robot_arm.controller.Position(x, y, z))
                print(f"Sent Inverse Kinematics Command: Position ({x}, {y}, {z})")

            for command in commands:
                command.start()
            for command in commands:
                command.join() # Wait for all threads to complete

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()