import sys
import tkinter as tk
from tkinter import Entry, scrolledtext

_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    if _model is not None:
        return True
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print("Loading Transformer model...")
        _tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
        _model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
        return True
    except Exception as e:
        print(f"Notice: Transformer model unavailable ({e}). Using rule-based fallback.")
        return False

def generate_fallback_response(message: str) -> str:
    msg = message.lower().strip()
    if any(w in msg for w in ["hello", "hi", "hey"]):
        return "Hello! How can I help you today?"
    elif "name" in msg:
        return "I am WebIdeasBot, your helpful AI assistant!"
    elif "help" in msg:
        return "I can assist you with answering questions, drafting ideas, or brainstorming."
    elif any(w in msg for w in ["bye", "exit", "quit"]):
        return "Goodbye! Have a wonderful day!"
    else:
        return f"Thank you for your message: '{message}'. How else can I assist you?"

def generate_response(message: str) -> str:
    if load_model():
        try:
            inputs = _tokenizer(message, return_tensors='pt', truncation=True)
            outputs = _model.generate(**inputs, max_length=150, pad_token_id=_tokenizer.eos_token_id)
            response = _tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception:
            return generate_fallback_response(message)
    else:
        return generate_fallback_response(message)

def run_gui():
    window = tk.Tk()
    window.title("WebIdeasBot")

    chat_window = scrolledtext.ScrolledText(window, width=80, height=20, state=tk.DISABLED)
    chat_window.pack(padx=10, pady=10)

    user_input = Entry(window, width=80)
    user_input.pack(padx=10, pady=10)
    user_input.focus_set()

    def on_send(event=None):
        message = user_input.get().strip()
        if message:
            chat_window.configure(state=tk.NORMAL)
            chat_window.insert(tk.END, f"You: {message}\n")
            chat_window.configure(state=tk.DISABLED)
            user_input.delete(0, tk.END)

            response = generate_response(message)
            chat_window.configure(state=tk.NORMAL)
            chat_window.insert(tk.END, f"WebIdeasBot: {response}\n\n")
            chat_window.configure(state=tk.DISABLED)
            chat_window.see(tk.END)

    user_input.bind("<Return>", on_send)
    window.mainloop()

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Query: {query}")
        print("Response:", generate_response(query))
    else:
        run_gui()

if __name__ == "__main__":
    main()

