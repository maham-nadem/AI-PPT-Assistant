import pyautogui
import keyboard
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

def control_ppt(gesture):
    if gesture == "next":
        keyboard.press_and_release("right")
        print(">> Next Slide")
    elif gesture == "prev":
        keyboard.press_and_release("left")
        print("<< Prev Slide")
    elif gesture == "pointer":
        print("☝️ Pointer Mode")
    elif gesture == "palm":
        keyboard.press_and_release("escape")
        print("✋ Palm - Stop")