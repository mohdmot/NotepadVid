# ascii_notepad_player.py
# متطلبات: opencv-python, pyperclip, pyautogui
# pip install opencv-python pyperclip pyautogui

import cv2
import numpy as np
import pyperclip
import pyautogui
import subprocess
import time
import sys

# --------------- Settings ----------------
VIDEO_PATH = "input.mp4"
OUT_HEIGHT = 120
FPS = 5
CHARS = "@%#*+=-:. "
# -----------------------------------------

def frame_to_ascii(frame, height=OUT_HEIGHT, chars=CHARS):
    # تحويل لصيغة grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    aspect_ratio = h / w
    
    new_h = height  # الارتفاع اللي تختاره أنت
    new_w = int(new_h / (aspect_ratio * 0.55))  # نحسب العرض بناءً على الارتفاع
    
    small = cv2.resize(gray, (new_w, new_h))
    # خرائط الحروف
    n_chars = len(chars)
    # بناء السلسلة
    lines = []
    for row in small:
        line = "".join(chars[int((pixel / 255) * (n_chars - 1))] for pixel in row)
        lines.append(line)
    return "\n".join(lines)

def open_and_maximize_notepad():
    # افتح notepad
    p = subprocess.Popen(["notepad.exe"])
    time.sleep(0.6)  # وقت للفتح
    # محاولة تكبير النافذة (Alt+Space ثم x)
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.05)
    pyautogui.press('x')
    time.sleep(0.2)
    return p

def play_video_in_notepad(path, fps=FPS):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Error: a problem in opening video file")
        return
    
    t1 = time.time()
    try:
        i = 1
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if not(i%3):
                ascii_frame = frame_to_ascii(frame)
                # انسخ للنص
                pyperclip.copy(ascii_frame + "\n"*10)
                #time.sleep(0.01)
                pyautogui.hotkey('ctrl', 'v')
            i+=1
    except KeyboardInterrupt:
        print("Stopped")
    finally:
        cap.release()
        # لا نغلق النوتباد تلقائياً حتى يشوف المستخدم النتيجة
        print(f"Finished in {time.time() - t1}s")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        VIDEO_PATH = sys.argv[1]
    time.sleep(1)
    open_and_maximize_notepad()
    time.sleep(2)
    play_video_in_notepad(VIDEO_PATH)

# main.py rickrolled.mp4