import sys
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

def get_definition(word: str) -> dict:
    """Fetch word definition and phonetics from Free Dictionary API."""
    word = word.strip().lower()
    if not word:
        return {"error": "Word cannot be empty."}

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return {"error": f"No definition found for '{word}'."}
        response.raise_for_status()
        data = response.json()

        meanings = []
        if isinstance(data, list) and len(data) > 0:
            entry = data[0]
            phonetic = entry.get('phonetic', '')
            for m in entry.get('meanings', []):
                part = m.get('partOfSpeech', 'meaning')
                defs = [d.get('definition', '') for d in m.get('definitions', []) if 'definition' in d]
                if defs:
                    meanings.append(f"[{part}] {defs[0]}")
            return {
                "word": word.capitalize(),
                "phonetic": phonetic,
                "definitions": meanings
            }
    except Exception as err:
        return {"error": f"Network error: {err}"}

    return {"error": "Unexpected error."}

def speak_text(text: str):
    """Convert text to speech audio."""
    if not text:
        return
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Output: {text}")

def search_and_speak(word: str) -> str:
    res = get_definition(word)
    if "error" in res:
        err_msg = res["error"]
        speak_text(err_msg)
        return err_msg

    output_lines = [f"Word: {res['word']} {res['phonetic']}\n"]
    for idx, d in enumerate(res['definitions'], 1):
        output_lines.append(f"{idx}. {d}")

    full_output = "\n".join(output_lines)
    speak_text(f"Definition for {res['word']}. " + " ".join(res['definitions']))
    return full_output

class SpeakingDictionaryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speaking Dictionary")
        self.root.geometry("550x450")

        header = tk.Label(self.root, text="Speaking Dictionary", font=("Arial", 18, "bold"))
        header.pack(pady=10)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter Word:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.focus_set()

        btn = tk.Button(input_frame, text="Search & Speak", font=("Arial", 11, "bold"), bg="navy", fg="white", command=self.on_search)
        btn.pack(side=tk.LEFT, padx=5)

        self.output_area = scrolledtext.ScrolledText(self.root, font=("Arial", 11), width=60, height=15)
        self.output_area.pack(pady=15, padx=15)

    def on_search(self):
        word = self.entry.get().strip()
        if not word:
            messagebox.showwarning("Input Error", "Please enter a word to search.")
            return

        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "Searching...\n")
        self.root.update()

        result = search_and_speak(word)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, result)
        self.output_area.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

def main():
    if len(sys.argv) > 1:
        word = sys.argv[1]
        print(search_and_speak(word))
    else:
        app = SpeakingDictionaryGUI()
        app.run()

if __name__ == '__main__':
    main()
