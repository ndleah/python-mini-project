# 📧 Improved Email Validator

This project provides a structured email validation script written in Python.  
It improves upon simple checks (like just searching for `@` and `.`) by applying multiple  
rules to accurately determine whether an email address is correctly formatted.

---

## 🚀 Features

### ✔ 1. Validates correct ordering of `@` and `.`
- Ensures `.` appears **after** `@`.
- Prevents invalid formats like:
  - `abc.gmail@com`
  - `@gmail.com`
  - `abc@gmail.`

### ✔ 2. Checks proper placement of characters
- Local part (before @) must not be empty.
- Domain must have a valid extension (like `.com`, `.in`, `.org`).

### ✔ 3. Handles spaces, dots, and case sensitivity
- Strips leading/trailing spaces.
- Converts email to lowercase.
- Detects consecutive dots such as `abc..xyz@gmail.com`.

### ✔ 4. Provides detailed error messages
Instead of printing just “invalid”, the validator explains *why* the email is invalid.

### ✔ 5. Uses regex + rule-based logic
A hybrid approach ensures both flexibility and safety.

---

## 🧪 Example Output
### Input

abc@gmail.com

### Output

✓ Email is valid!

### Input

@domain.com

### Output

✗ Email is invalid due to:
 - Email must contain text before '@'.
 - Email contains invalid characters or structure.

##  How to Run

```bash
python email_validator.py