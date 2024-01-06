import tkinter as tk
from tkinter import Entry, scrolledtext
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-1_5", trust_remote_code=True)

# Function to generate a response from the model


def generate_response(message):
    inputs = tokenizer(message, return_tensors='pt', truncation=True)
    outputs = model.generate(
        **inputs,
        max_length=150,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to handle when the user sends a message


def on_send(event=None):  # event is passed by binders.
    message = user_input.get()
    if message:  # Only process if there's a message
        # Display user message in the chat window
        chat_window.configure(state=tk.NORMAL)  # Temporarily make it editable
        chat_window.insert(tk.END, f"You: {message}\n")
        chat_window.configure(state=tk.DISABLED)  # Make it read-only again

        # Clear the user input field
        user_input.delete(0, tk.END)

        # Generate and display chatbot response
        response = generate_response(message)
        chat_window.configure(state=tk.NORMAL)
        chat_window.insert(tk.END, f"WebIdeasBot: {response}\n")
        chat_window.configure(state=tk.DISABLED)


# Create the main window
window = tk.Tk()
window.title("WebIdeasBot")

# Create the chat window
chat_window = scrolledtext.ScrolledText(
    window, width=80, height=20, state=tk.DISABLED)
chat_window.pack()

# Create the user input field
user_input = Entry(window, width=80)
user_input.pack()
user_input.focus_set()  # Set focus to the input field

# Bind the Enter key to the on_send function
user_input.bind("<Return>", on_send)

# Start the Tkinter event loop
window.mainloop()
