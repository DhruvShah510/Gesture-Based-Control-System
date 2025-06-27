# Gesture-Based-Control-System

A **Gesture Based Control System** using **Tkinter, OpenCV, and MediaPipe** that enables **hands-free interaction with your system**. It allows you to:

- 📶 **Control system volume** using finger gestures.
- ✌️ **Recognize hand gestures** like Fist, Peace, Pointing, and Open Hand.
- ✋ **Count the number of fingers** shown in front of the camera.

This project demonstrates **real-time computer vision**, **human-computer interaction**, and **gesture recognition pipelines** in a clean, modular, and research-friendly structure. Ideal for **learning, demos, academic projects, and future gesture-based control extensions**.

---

## 🚀 Features

**Live camera-based gesture recognition**  
**Volume control using gestures**  
**Gesture classification** (Fist, Peace, Pointing, Open Hand)  
**Finger counting with support for two hands**  
**Clean Tkinter GUI navigation with Back button**  
**Real-time visual feedback with overlays**  
**Modular, readable code for easy extension**

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** (GUI)
- **OpenCV** (Video capture and processing)
- **MediaPipe** (Hand tracking)
- **Pillow** (Image handling for Tkinter)
- **PyCaw** (Windows volume control)

---

## 📁 Project Structure
├── **main.py** - Entry point for GUI
├── **gesture_selector_gui.py** - Main task selection GUI
├── **volume_controller_gui.py** - Volume control window
├── **gesture_recognizer.py** - Gesture recognition window
├── **finger_counter.py** - Finger counting window
│
├── hand_tracker.py # Hand tracking utility File with all necessary finctions 
├── volume_controller.py # System volume controller file 
├── utils.py # Utility functions for calculating euclidian distance 

---

## ⚙️ Installation

1️) Clone the Repository
2️) Create and Activate Virtual Environment (Recommended)  
3️) Install Dependencies


## 🖥️ Usage
Run the application:
python main.py

You will see a home GUI with three options:

1️) Volume Control
2️) Gesture Recognition
3️) Finger Counter

Click on any task to launch it in real time. Use the Back button to return to the home screen and select another task seamlessly. 

## 💡 How It Works
**Hand Tracking:** Uses MediaPipe to detect and track hand landmarks in real-time.
**Gesture Recognition:** Checks finger landmark positions to identify gestures (e.g., Fist, Peace).
**Volume Control:** Maps the distance between thumb and index finger to system volume levels using PyCaw.
**Finger Counter:** Counts the number of fingers raised on either hand.

## ✨ Acknowledgements
MediaPipe
OpenCV
PyCaw

🙌 Author
Dhruv Shah
🌐 LinkedIn - https://www.linkedin.com/in/dhruv-shah-25997624b

⭐ If you find this project useful, please give it a star!



