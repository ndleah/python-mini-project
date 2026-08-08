import os
import sys
import json
import tkinter as tk 
from tkinter import messagebox
from difflib import get_close_matches

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def access_data(file_path=DATA_FILE):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: data.json file not found in script directory.")
        return {}
    except json.JSONDecodeError:
        print("Error: Unable to decode data.json file.")
        return {}

def translate(word, file_data):
    if not file_data:
        return "Dictionary data is empty or missing.", None

    word = word.lower().strip()
    if word in file_data:
        return file_data[word], None
    elif word.title() in file_data:
        return file_data[word.title()], None
    elif word.upper() in file_data:
        return file_data[word.upper()], None
    else:
        matches = get_close_matches(word, file_data.keys())
        if len(matches) > 0:
            return f"Did you mean '{matches[0]}' instead?", matches[0]
        else:
            return "The word does not exist. Please double-check it.", None

def run_gui(file_data):
    root = tk.Tk()
    root.title("Dictionary")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Enter a word:")
    label.pack()

    entry = tk.Entry(frame, width=50)
    entry.pack(pady=5)
    entry.focus_set()

    result_label = tk.Label(frame, text="", wraplength=400, justify="left")
    suggest_button = tk.Button(frame, text="", wraplength=400, justify="left")

    def on_search():
        word = entry.get().strip()
        if word:
            output, suggestion = translate(word, file_data)
            if isinstance(output, list):
                result_text = '\n'.join(output)
            else:
                result_text = output
            result_label.config(text=result_text)

            if suggestion:
                def suggest():
                    suggested_output, _ = translate(suggestion, file_data)
                    if isinstance(suggested_output, list):
                        result_label.config(text='\n'.join(suggested_output))
                    else:
                        result_label.config(text=suggested_output)
                    suggest_button.pack_forget()

                suggest_button.config(command=suggest, text=f"Search for '{suggestion}'")
                suggest_button.pack(pady=5)
            else:
                suggest_button.pack_forget()
        else:
            messagebox.showwarning("Input Error", "Please enter a word to search.")

    search_button = tk.Button(frame, text="Search", command=on_search)
    search_button.pack(pady=5)

    result_label.pack(pady=10)

    root.bind('<Return>', lambda e: on_search())
    root.mainloop()

def main():
    file_data = access_data(DATA_FILE)
    if len(sys.argv) > 1:
        word = ' '.join(sys.argv[1:])
        output, _ = translate(word, file_data)
        if isinstance(output, list):
            for item in output:
                print(item)
        else:
            print(output)
    else:
        run_gui(file_data)

if __name__ == "__main__":
    main()

