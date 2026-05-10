import keyboard

def control_ppt(gesture):
    if gesture == "next":
        keyboard.press_and_release("right")
        print(">> Next Slide")
    elif gesture == "prev":
        keyboard.press_and_release("left")
        print("<< Prev Slide")
    elif gesture == "pointer":
        print("Pointer ON")
    elif gesture == "palm":
        print("Pointer OFF")