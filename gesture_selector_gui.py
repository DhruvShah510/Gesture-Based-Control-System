import tkinter as tk
from volume_controller_gui import HandGestureGUI
from gesture_recognizer import HandGestureRecognizerGUI
from finger_counter import FingerCounterGUI

class GestureSelectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture System")
        self.root.geometry("800x600")

        tk.Label(root, text="Choose a Task", font=("Arial", 16)).pack(pady=20)

        tk.Button(root, text="1. Volume Control", command=self.launch_volume_control).pack(pady=10)
        tk.Button(root, text="2. Gesture Recognition", command=self.launch_gesture_recognition).pack(pady=10)
        tk.Button(root, text="3. Finger Counter", command=self.launch_finger_counter).pack(pady=10)

    def launch_volume_control(self):
        self.root.withdraw()
        top = tk.Toplevel()
        HandGestureGUI(top, self.root)

    def launch_gesture_recognition(self):
        self.root.withdraw()
        top = tk.Toplevel()
        HandGestureRecognizerGUI(top, self.root)

    def launch_finger_counter(self):
        self.root.withdraw()
        top = tk.Toplevel()
        FingerCounterGUI(top, self.root)


    