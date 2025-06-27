import tkinter as tk
import cv2
from PIL import Image, ImageTk
from hand_tracker import HandTracker
import sys

class HandGestureRecognizerGUI:
    def __init__(self, root, parent_root):
        self.root = root
        self.parent_root = parent_root
        self.root.title("Hand Gesture Recognizer")
        self.root.geometry("800x600")
        self.running = True

        self.label = tk.Label(root)
        self.label.pack(pady=10)

        self.gesture_label = tk.Label(root, text="Gesture: ", font=("Arial", 16))
        self.gesture_label.pack(pady=5)

        self.back_button = tk.Button(root, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.detector = HandTracker()


        #here
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_frame()

    def go_back(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        self.parent_root.deiconify()
        

    def update_frame(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = self.detector.find_hands(frame)
                landmarks = self.detector.get_landmark_positions(frame)

                gesture = "Unknown"
                if landmarks:
                    fingers_up = self.get_finger_states(landmarks)
                    total_up = sum(fingers_up)

                    if total_up == 0:
                        gesture = "Fist"
                    elif total_up == 2 and fingers_up[1] and fingers_up[2]:
                        gesture = "Peace"
                    elif total_up == 5:
                        gesture = "Open Hand"
                    elif total_up == 1 and fingers_up[1]:
                        gesture = "Pointing"

                self.gesture_label.config(text=f"Gesture: {gesture}")

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.config(image=imgtk)

        if self.running:
            self.root.after(15, self.update_frame)

    def get_finger_states(self, lm):
        tips = [4, 8, 12, 16, 20]
        fingers = []
        fingers.append(lm[4][1] > lm[3][1])
        for tip in tips[1:]:
            fingers.append(lm[tip][2] < lm[tip - 2][2])
        return fingers


    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        sys.exit(0)
