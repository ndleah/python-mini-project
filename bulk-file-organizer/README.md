# 🗂️ Bulk File Organizer — Integration Module

**Bulk File Organizer** is a Python command-line tool that automatically sorts files in a directory based on their extensions.
It transforms digital clutter into clean, structured folders — with vibrant terminal feedback powered by **Rich** ✨

---

## 📣 Latest Update: Integrated Module

This release brings integration with the [Bulk File Organizer](https://github.com/Shravan250/bulk-file-organizer) — a CLI utility by [Shravan Bobade](https://github.com/Shravan250) that organizes files by type, supports dry-run simulations, and provides colorful output using the `rich` library.

### ✨ Highlights

- 📦 Automatically sorts files into categorized folders (Images, Documents, Archives, etc.)
- 🔁 Recursive directory scanning
- 🧪 Dry-run simulation mode (no files moved)
- 🌈 Beautiful progress bars & summary tables
- ⚙️ Extensible via custom mappings

---

## ⚙️ Installation

```bash
pip install bulk-file-organizer
```

Or install directly from source:

```bash
git clone https://github.com/Shravan250/bulk-file-organizer.git
cd bulk-file-organizer
pip install .
```

---

## 🖥️ Usage

```bash
bulk-organizer /path/to/your/folder
```

### Options

| Flag          | Description                                |
| ------------- | ------------------------------------------ |
| `--dry-run`   | Simulate organization without moving files |
| `--summary`   | Display a summary table after organization |
| `--recursive` | Recursively organize subdirectories        |
| `--version`   | Display the current version                |

#### Example

```bash
bulk-organizer ~/Downloads --dry-run --summary
```

---

## 🧠 Example Output

```text
──────────────────────────── Bulk Organizer v0.1.0 ─────────────────────────────
Target Directory: ~/Downloads

Dry Run Mode Enabled — no files will be moved.

✨ Organizing files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02

📊 Organization Summary

┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Folder    ┃ File Count ┃ Example Files                ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Images    │ 12         │ photo.png, logo.jpg, …       │
│ Documents │ 8          │ resume.pdf, notes.txt, …     │
│ Archives  │ 2          │ backup.zip, logs.tar.gz      │
└───────────┴────────────┴──────────────────────────────┘
──────────────────────────── Operation Complete ─────────────────────────────
```

---

## 🧩 Project Structure

```
bulk-file-organizer/
│
├── bulk_organizer/
│   ├── __init__.py
│   ├── cli.py
│   ├── scanner.py
│   ├── mapper.py
│   ├── organizer.py
│   └── utils.py
│
├── tests/
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🤝 Contributing

We love clean code and clever minds.
Check out the [CONTRIBUTING.md](https://github.com/Shravan250/bulk-file-organizer/blob/main/CONTRIBUTING.md) to learn how you can contribute and make this project even better.

---

## 🪪 License

Licensed under the **MIT License**.

---

## ⭐ Show Some Love

If this project helped you bring order to your chaos —
please consider giving it a ⭐ on [GitHub](https://github.com/Shravan250/bulk-file-organizer)!
Every star helps this project grow and keeps the world just a little more organized 🌍✨
