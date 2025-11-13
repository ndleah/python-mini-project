# Project Title: GenAI Poem Generator

## 🛠️ Description
The **GenAI Poem Generator** is a creative Python mini-project that uses a **Generative AI model** to compose short poems based on a user-provided theme.  
It leverages the **TinyLlama-1.1B-Chat** model from Hugging Face to create vivid, imaginative poetry in various styles (haiku, sonnet, free verse, etc.).  
The project also includes an **offline fallback poet**, so users can still generate poems without requiring model downloads or internet access.

This project was created as part of an open-source contribution to the repository [`ndleah/python-mini-project`](https://github.com/ndleah/python-mini-project).

---

## ⚙️ Installation / Requirements
To run this project, make sure you have Python 3.8+ installed.  
Install dependencies by running:

```bash
pip install -r requirements.txt

**Required Libraries:**

- transformers

- torch

- pytest

**Usage**

After installing the dependencies, navigate to the project directory and run:

**python main.py "first rain on campus" --form haiku --lines 3**

**Example Output:**

Rain's first glee,
Cushions feet in fields,
Lilies unfurled from dorms.


You can customize the poem’s form and number of lines:

**python main.py "evening coffee" --form sonnet --lines 4**
