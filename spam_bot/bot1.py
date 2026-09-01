
import sys
import time

def spammingBot(string: str, count: int = 5, delay: float = 1.0):
    """Safely type message via pyautogui if available, otherwise print."""
    if not string:
        print("Error: Empty string provided.")
        return

    try:
        import pyautogui as pyg
        import keyboard as kbd
        print("Press 'q' at any time to stop spamming.")
        for i in range(count):
            if kbd.is_pressed('q'):
                print("Spamming stopped by user.")
                break
            pyg.typewrite(string)
            pyg.press("enter")
            time.sleep(delay)
    except (ImportError, Exception) as e:
        print(f"CLI Mode - Spammed ({count}x): {string}")

def main():
    string = input("Enter text to spam: ").strip()
    if string:
        print("Starting in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        spammingBot(string)

if __name__ == '__main__':
    main()