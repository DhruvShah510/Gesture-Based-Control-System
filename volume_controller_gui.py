import tkinter as tk
import cv2
from PIL import Image, ImageTk
from hand_tracker import HandTracker
from volume_controller import VolumeController
from utils import calculate_distance
import sys

class HandGestureGUI:
    def __init__(self, root, parent_root):
        self.root = root
        self.parent_root = parent_root
        self.root.title("Hand Gesture Volume Controller")
        self.root.geometry("800x600")
        self.running = True

        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)

        # self.volume_label = tk.Label(root, text="Volume: 0%", font=("Arial", 14))
        # self.volume_label.pack()

        self.back_button = tk.Button(root, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.detector = HandTracker()
        self.volume_ctrl = VolumeController()

        # here
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_video()

    def go_back(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        self.parent_root.deiconify()

    def update_video(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = self.detector.find_hands(frame)
                landmarks = self.detector.get_landmark_positions(frame)

                if landmarks:
                    x1, y1 = landmarks[4][1], landmarks[4][2]
                    x2, y2 = landmarks[8][1], landmarks[8][2]
                    cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                    cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    self.volume_ctrl.set_volume_by_distance(
                        distance=calculate_distance((x1, y1), (x2, y2))
                    )
                    # vol_percent = self.volume_ctrl.get_volume_percent()
                    # self.volume_label.config(text=f"Volume: {vol_percent}%")

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)

        if self.running:
            self.root.after(15, self.update_video)


    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        sys.exit(0)
