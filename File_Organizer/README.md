<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# File Organizer

## 🛠️ Description

A command-line utility that automatically sorts files in a directory into categorized subfolders based on their file extension. Supports a **dry-run mode** to preview changes before anything is moved.

**Categories organized:**

| Folder | Extensions |
|---|---|
| Images | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` `.ico` `.tiff` |
| Videos | `.mp4` `.mkv` `.mov` `.avi` `.wmv` `.flv` `.webm` `.m4v` |
| Audio | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.wma` `.m4a` |
| Documents | `.pdf` `.doc` `.docx` `.xls` `.xlsx` `.ppt` `.pptx` `.txt` `.odt` `.csv` |
| Archives | `.zip` `.tar` `.gz` `.rar` `.7z` `.bz2` `.xz` |
| Code | `.py` `.js` `.ts` `.html` `.css` `.java` `.c` `.cpp` `.go` `.rb` `.rs` `.sh` |
| Data | `.json` `.xml` `.yaml` `.yml` `.sql` `.db` `.sqlite` |
| Executables | `.exe` `.msi` `.dmg` `.deb` `.rpm` `.apk` |
| Fonts | `.ttf` `.otf` `.woff` `.woff2` |
| Misc | Everything else |

## ⚙️ Languages or Frameworks Used

- Python 3 (standard library only — no dependencies required)

## 🌟 How to run

Organize your current directory:

```bash
python file_organizer.py
```

Organize a specific directory:

```bash
python file_organizer.py /path/to/your/folder
```

Preview changes without moving anything (dry run):

```bash
python file_organizer.py /path/to/your/folder --dry-run
```

## 📺 Demo

```
=============================================
  Directory : /Users/user/Downloads
  Moved     : 12 file(s)
=============================================

  Archives/ (2 file(s))
    - project.zip
    - backup.tar.gz

  Documents/ (4 file(s))
    - report.pdf
    - notes.txt
    - budget.xlsx
    - slides.pptx

  Images/ (3 file(s))
    - photo.jpg
    - banner.png
    - logo.svg

  Videos/ (3 file(s))
    - demo.mp4
    - tutorial.mkv
    - clip.mov
```

## 🤖 Author

[Uchebuzz](https://github.com/Uchebuzz)
