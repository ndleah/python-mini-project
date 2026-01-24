# Palindrome Checker (Python)

A simple interactive Python program that checks whether a **word** is a palindrome or finds **palindromic words within a sentence**. The program runs in the terminal and allows repeated checks without restarting.

---

## 📌 Features

- Check if a **single word** is a palindrome
- Scan a **sentence** and detect all palindromic words
- Case-insensitive comparisons
- Ignores punctuation in sentence checks
- User-friendly input validation using `pyinputplus`
- Option to rerun the program indefinitely until the user exits

---

## 🧠 What Is a Palindrome?

A palindrome is a word that reads the same forwards and backwards.

Examples:
- racecar
- level
- madam

---

## 🛠 Requirements

- Python 3.x
- pyinputplus module

Install the required dependency with:

pip install pyinputplus

---

## ▶️ How to Run

1. Save the script as `palindrome_checker.py`
2. Open a terminal in the same directory
3. Run:

python palindrome_checker.py

---

## 🧪 How It Works

### Word Check
- Prompts the user to enter a word
- Converts it to lowercase
- Reverses the word using slicing
- Compares the original and reversed word

### Sentence Check
- Prompts the user to enter a sentence
- Converts it to lowercase
- Removes punctuation
- Splits the sentence into words
- Identifies and lists palindromic words

---

## 🔁 Program Flow

1. User selects:
   - [1] Check a word
   - [2] Check a sentence
2. Program performs the selected check
3. User is asked whether they want to run another check
4. Program continues until the user chooses to exit

---

## 📂 Example Output

Check a [1] Word or [2] Sentence?
1

What word would you like to check?
racecar

The word "racecar" is a palindrome!

---

## 📄 License

This project is open-source and free to use for learning or personal projects.
