![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# File Organizer

## 🛠️ Description

A simple Python script that organizes messy folders by sorting files into subfolders based on their file type. It supports 8 categories like Images, Documents, Videos, Audio, Code, etc. Also has an undo feature to reverse the organization if needed.

## ⚙️ Languages or Frameworks Used

You only need Python 3 to run this script. No extra libraries needed — it uses only built-in modules (`os`, `shutil`, `json`).

You can visit [here](https://www.python.org/downloads/) to download Python.

## 🌟 How to run

Organize files in the current directory:

```sh
python file_organizer.py
```

Organize a specific folder:

```sh
python file_organizer.py /path/to/folder
```

Undo the last organization:

```sh
python file_organizer.py --undo
```

## 📺 Demo

**Before:**
```
Downloads/
├── report.pdf
├── photo.jpg
├── song.mp3
├── script.py
├── movie.mp4
└── data.csv
```

**After running the script:**
```
Downloads/
├── Documents/
│   ├── report.pdf
│   └── data.csv
├── Images/
│   └── photo.jpg
├── Audio/
│   └── song.mp3
├── Code/
│   └── script.py
└── Videos/
    └── movie.mp4
```

## 🤖 Author

[Kaligotla Sri Datta Sai Vithal](https://github.com/Sridattasai18)
