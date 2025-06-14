import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from hand_tracker import HandTracker

class FingerCounterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finger Counter")
        self.root.geometry("800x600")
        self.running = False

        self.label = tk.Label(root)
        self.label.pack(pady=10)

        self.count_label = tk.Label(root, text="Fingers: 0", font=("Arial", 16))
        self.count_label.pack(pady=5)

        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()

        self.cap = None
        self.detector = HandTracker(max_num_hands=2)

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

            total = 0
            h, w, _ = frame.shape

            # ✅ Iterate through all detected hands and their handedness
            if self.detector.results.multi_hand_landmarks:
                for hand_lm, hand_handedness in zip(self.detector.results.multi_hand_landmarks, self.detector.results.multi_handedness):
                    label = hand_handedness.classification[0].label  # 'Right' or 'Left'
                    lm = [(i, int(lm.x * w), int(lm.y * h), lm.x) for i, lm in enumerate(hand_lm.landmark)]  # Include raw x
                    total += sum(self.get_finger_states(lm, label))

            self.count_label.config(text=f"Fingers: {total}")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)

            self.root.after(15, self.update_frame)

    # ✅ Updated: get_finger_states now takes label
    def get_finger_states(self, lm, label):
        tips = [4, 8, 12, 16, 20]
        fingers = []

        # ✅ Thumb: compare x values based on hand
        thumb_tip_x = lm[4][3]
        thumb_ip_x = lm[3][3]

        if label == "Right":
            fingers.append(thumb_tip_x < thumb_ip_x)  # Thumb pointing left (open)
        else:
            fingers.append(thumb_tip_x > thumb_ip_x)  # Thumb pointing right (open)

        # ✅ Other fingers: compare y values (tip higher than pip joint)
        for tip in tips[1:]:
            fingers.append(lm[tip][2] < lm[tip - 2][2])  # tip_y < pip_y

        return fingers
