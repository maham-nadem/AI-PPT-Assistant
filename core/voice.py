import speech_recognition as sr
import threading
import keyboard
import pyautogui
import time
import subprocess
import os
from core.llm_processor import process_with_llm

recognizer = sr.Recognizer()
recognizer.energy_threshold = 400
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

def execute_command(command):
    action = command.get("action", "none")

    # ── NAVIGATION ────────────────────────────
    if action == "next":
        keyboard.press_and_release("right")
        print(">> Next Slide")

    elif action == "prev":
        keyboard.press_and_release("left")
        print("<< Prev Slide")

    elif action == "stop":
        keyboard.press_and_release("escape")
        print("✋ Stop")

    elif action == "present":
        keyboard.press_and_release("f5")
        print("▶️ Present")

    # ── SLIDES ────────────────────────────────
    elif action == "new_slide":
        keyboard.press_and_release("ctrl+m")
        print("📄 New Slide")

    elif action == "save":
        keyboard.press_and_release("ctrl+s")
        print("💾 Save")

    elif action == "undo":
        keyboard.press_and_release("ctrl+z")
        print("↩️ Undo")

    elif action == "redo":
        keyboard.press_and_release("ctrl+y")
        print("↪️ Redo")

    # ── TYPING ────────────────────────────────
    elif action == "type":
        text = command.get("text", "")
        if text:
            pyautogui.typewrite(text, interval=0.04)
            print(f"✍️ Typed: {text}")

    # ── FORMATTING ────────────────────────────
    elif action == "bold":
        keyboard.press_and_release("ctrl+b")
        print("Bold ✅")

    elif action == "italic":
        keyboard.press_and_release("ctrl+i")
        print("Italic ✅")

    elif action == "underline":
        keyboard.press_and_release("ctrl+u")
        print("Underline ✅")

    elif action == "center":
        keyboard.press_and_release("ctrl+e")
        print("Center ✅")

    elif action == "left_align":
        keyboard.press_and_release("ctrl+l")
        print("Left align ✅")

    elif action == "right_align":
        keyboard.press_and_release("ctrl+r")
        print("Right align ✅")

    elif action == "select_all":
        keyboard.press_and_release("ctrl+a")
        print("Selected all ✅")

    elif action == "delete":
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.1)
        keyboard.press_and_release("delete")
        print("🗑️ Deleted")

    elif action == "copy":
        keyboard.press_and_release("ctrl+c")
        print("Copy ✅")

    elif action == "paste":
        keyboard.press_and_release("ctrl+v")
        print("Paste ✅")

    elif action == "cut":
        keyboard.press_and_release("ctrl+x")
        print("Cut ✅")

    # ── FONT SIZE ─────────────────────────────
    elif action == "font_size":
        size = command.get("size", 24)
        # Alt+H → FS → size type karo
        keyboard.press_and_release("alt+h")
        time.sleep(0.3)
        keyboard.press_and_release("alt+h,fs")
        time.sleep(0.3)
        pyautogui.typewrite(str(size), interval=0.05)
        keyboard.press_and_release("enter")
        print(f"Font size: {size}")

    # ── FONT COLOR ────────────────────────────
    elif action == "font_color":
        color = command.get("color", "")
        print(f"🎨 Font color: {color} — Manual select karo")
        keyboard.press_and_release("alt+h")
        time.sleep(0.3)

    # ── BACKGROUND ────────────────────────────
    elif action == "background":
        color = command.get("color", "")
        print(f"🎨 Background: {color}")
        keyboard.press_and_release("alt+g")
        time.sleep(0.5)

    # ── TABS ──────────────────────────────────
    elif action == "home_tab":
        keyboard.press_and_release("alt+h")
        print("🏠 Home tab")

    elif action == "insert_tab":
        keyboard.press_and_release("alt+n")
        print("➕ Insert tab")

    elif action == "design_tab":
        keyboard.press_and_release("alt+g")
        print("🎨 Design tab")

    elif action == "transitions_tab":
        keyboard.press_and_release("alt+k")
        print("🔄 Transitions tab")

    elif action == "animations_tab":
        keyboard.press_and_release("alt+a")
        print("✨ Animations tab")

    elif action == "view_tab":
        keyboard.press_and_release("alt+w")
        print("👁️ View tab")

    # ── INSERT ────────────────────────────────
    elif action == "insert_table":
        rows = command.get("rows", 3)
        cols = command.get("cols", 3)
        keyboard.press_and_release("alt+n")
        time.sleep(0.3)
        keyboard.press_and_release("alt+n,t")
        print(f"📊 Table {rows}x{cols}")

    elif action == "insert_chart":
        keyboard.press_and_release("alt+n")
        time.sleep(0.3)
        keyboard.press_and_release("alt+n,c")
        print("📈 Chart")

    elif action == "insert_textbox":
        keyboard.press_and_release("alt+n")
        time.sleep(0.3)
        keyboard.press_and_release("alt+n,x")
        print("📝 Textbox")

    elif action == "insert_image":
        query = command.get("query", "")
        keyboard.press_and_release("alt+n")
        time.sleep(0.3)
        keyboard.press_and_release("alt+n,p")
        print(f"🖼️ Image: {query}")

    # ── ZOOM ──────────────────────────────────
    elif action == "zoom_in":
        keyboard.press_and_release("alt+w")
        time.sleep(0.3)
        print("🔍 Zoom in")

    elif action == "zoom_out":
        keyboard.press_and_release("alt+w")
        time.sleep(0.3)
        print("🔍 Zoom out")

    elif action == "none":
        pass

def listen_loop():
    print("🎤 LLM Voice ready!")
    print("Kuch bhi bolo — Urdu/English — sab samjhega!")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, timeout=3,
                                         phrase_time_limit=6)
                text = recognizer.recognize_google(
                    audio, language="en-US")
                print(f"🎤 Voice: {text}")
                command = process_with_llm(text)
                execute_command(command)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception:
                pass

def start_voice():
    t = threading.Thread(target=listen_loop, daemon=True)
    t.start()