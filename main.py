# # main.py

# import tkinter as tk
# from gui import HandGestureGUI

# def main():
#     root = tk.Tk()
#     app = HandGestureGUI(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()

# main.py
import tkinter as tk
from gesture_selector_gui import GestureSelectorGUI

def main():
    root = tk.Tk()
    app = GestureSelectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
