import speech_recognition as sr
import threading
import keyboard

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

COMMANDS = {
    "next":    ["next", "next Slide"],
    "prev":    ["back", "previous", "Previous Slide"],
    "stop":    ["stop", "band", "exit"],
    "pointer": ["pointer", "point"],
}

def process_command(text):
    text = text.lower().strip()
    print(f"🎤 Voice: {text}")
    for action, keywords in COMMANDS.items():
        for word in keywords:
            if word in text:
                if action == "next":
                    keyboard.press_and_release("right")
                    print(">> Voice: Next Slide")
                elif action == "prev":
                    keyboard.press_and_release("left")
                    print("<< Voice: Prev Slide")
                elif action == "stop":
                    keyboard.press_and_release("escape")
                    print("✋ Voice: Stop")
                return

def listen_loop():
    print("🎤 Voice ready! Bol sako: next, back, stop")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, timeout=3,
                                         phrase_time_limit=2)
                text = recognizer.recognize_google(audio,
                                                   language="en-US")
                process_command(text)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception:
                pass

def start_voice():
    t = threading.Thread(target=listen_loop, daemon=True)
    t.start()