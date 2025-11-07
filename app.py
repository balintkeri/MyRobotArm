
import tkinter as tk

from Controller import RobotArm

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
            angle_entry = tk.Entry(self.anglegridFrame, width=10)
            angle_entry.insert(0, str(i.angle))
            angle_entry.bind("<Return>", self.sendCommand)
            angle_entry.grid(row=node_id, column=1, padx=5, pady=5)
            self.angleEntries.append(angle_entry)


        self.exitButton = tk.Button(root, text="Exit", command=self.cleanup)
        self.exitButton.pack(pady=10)

        self.magnetOnButton = tk.Button(root, text="Magnet On", command=self.robot_arm.magnetOn)
        self.magnetOnButton.pack(pady=5)
        self.magnetOffButton = tk.Button(root, text="Magnet Off", command=self.robot_arm.magnetOff)
        self.magnetOffButton.pack(pady=5)


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
                self.robot_arm.command(angles=[float(entry.get()) for entry in self.angleEntries])
            else:
                position_str = self.positionEntry.get()
                x, y, z = map(float, position_str.split(','))
                self.robot_arm.command(position=self.robot_arm.controller.Position(x, y, z))
                print(f"Sent Inverse Kinematics Command: Position ({x}, {y}, {z})")


        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()