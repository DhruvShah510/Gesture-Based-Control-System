# gesture_recognizer.py

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from hand_tracker import HandTracker

class HandGestureRecognizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Recognizer")
        self.root.geometry("800x600")
        self.running = False

        self.label = tk.Label(root)
        self.label.pack(pady=10)

        self.gesture_label = tk.Label(root, text="Gesture: ", font=("Arial", 16))
        self.gesture_label.pack(pady=5)

        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()

        self.cap = None
        self.detector = HandTracker()

    def start(self):
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture(0)
            self.update_frame()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.label.config(image='')

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if not ret:
                return

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
                    gesture = "Peace ✌️"
                elif total_up == 5:
                    gesture = "Open Hand 🖐️"
                elif total_up == 1 and fingers_up[1]:
                    gesture = "Pointing ☝️"

            self.gesture_label.config(text=f"Gesture: {gesture}")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)

            self.root.after(15, self.update_frame)

    def get_finger_states(self, lm):
        tips = [4, 8, 12, 16, 20]
        fingers = []
        # Thumb (x-axis)
        fingers.append(lm[4][1] > lm[3][1])
        # Other fingers (y-axis)
        for tip in tips[1:]:
            fingers.append(lm[tip][2] < lm[tip - 2][2])
        return fingers