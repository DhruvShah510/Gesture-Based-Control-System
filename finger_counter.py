import tkinter as tk
import cv2
from PIL import Image, ImageTk
from hand_tracker import HandTracker
import sys

class FingerCounterGUI:
    def __init__(self, root, parent_root):
        self.root = root
        self.parent_root = parent_root
        self.root.title("Finger Counter")
        self.root.geometry("800x600")
        self.running = True

        self.label = tk.Label(root)
        self.label.pack(pady=10)

        self.count_label = tk.Label(root, text="Fingers: 0", font=("Arial", 16))
        self.count_label.pack(pady=5)

        self.back_button = tk.Button(root, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.detector = HandTracker(max_num_hands=2)

        # here
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

                total = 0
                h, w, _ = frame.shape

                if self.detector.results.multi_hand_landmarks:
                    for hand_lm, hand_handedness in zip(self.detector.results.multi_hand_landmarks, self.detector.results.multi_handedness):
                        label = hand_handedness.classification[0].label
                        lm = [(i, int(lm.x * w), int(lm.y * h), lm.x) for i, lm in enumerate(hand_lm.landmark)]
                        total += sum(self.get_finger_states(lm, label))

                self.count_label.config(text=f"Fingers: {total}")

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.config(image=imgtk)

        if self.running:
            self.root.after(15, self.update_frame)

    def get_finger_states(self, lm, label):
        tips = [4, 8, 12, 16, 20]
        fingers = []

        thumb_tip_x = lm[4][3]
        thumb_ip_x = lm[3][3]
        if label == "Right":
            fingers.append(thumb_tip_x < thumb_ip_x)
        else:
            fingers.append(thumb_tip_x > thumb_ip_x)

        for tip in tips[1:]:
            fingers.append(lm[tip][2] < lm[tip - 2][2])
        return fingers

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        sys.exit(0)
