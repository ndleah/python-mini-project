import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")

        self.questions = [
            {
                'question': 'What is the capital of France?',
                'options': ['Paris', 'London', 'Madrid', 'Rome'],
                'correct_index': 0
            },
            {
                'question': "Which planet is known as the 'Red Planet'?",
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'correct_index': 1
            },
            # Add more questions
        ]

        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(root, text='', font=('Helvetica', 16))
        self.question_label.pack(pady=20)

        self.options_buttons = []
        for i in range(4):
            button = tk.Button(root, text='', font=('Helvetica', 12), command=lambda i=i: self.check_answer(i))
            self.options_buttons.append(button)
            button.pack(fill='x', padx=20, pady=5)

        self.load_question()

    def load_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=question['question'])

        for i in range(4):
            self.options_buttons[i].config(text=question['options'][i])

    def check_answer(self, selected_index):
        correct_index = self.questions[self.current_question]['correct_index']
        
        if selected_index == correct_index:
            self.score += 1

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        result_text = f"Your Score: {self.score}/{len(self.questions)}"
        messagebox.showinfo("Quiz Result", result_text)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
