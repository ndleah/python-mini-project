# Bulk File Renamer

## 🛠️ Description
A simple CLI tool to bulk rename files in a folder using a custom pattern.  
Perfect for organizing photos (`trip_1.jpg`, `trip_2.jpg`), notes, or any file batch.

**Example:** Rename `IMG_1234.jpg`, `IMG_5678.jpg` → `vacation_1.jpg`, `vacation_2.jpg`

## ⚙️ Languages or Frameworks Used
- Python 3 (standard library only)
- `pathlib` for cross-platform file handling
- No external dependencies

## 🌟 How to run
1. Save as `bulk_file_renamer.py`
2. Open terminal in folder with files to rename
3. Run: `python bulk_file_renamer.py`

**Interactive prompts will guide you:**
Enter folder path: [current folder]
Enter extension: .jpg
Enter base name: vacation
Starting number: 1
[Preview shown]
Proceed? [y/N]

## 📺 Demo
🔄 Bulk File Renamer
Enter folder path:
Enter file extension: .jpg
📁 Found 3 files:

IMG_001.jpg

IMG_002.jpg

IMG_003.jpg

Enter base name: trip
Starting number: 1

==================================================
PREVIEW (what will be renamed):
IMG_001.jpg → trip_1.jpg
IMG_002.jpg → trip_2.jpg
IMG_003.jpg → trip_3.jpg
Proceed with rename? [y/N]: y
✅ IMG_001.jpg → trip_1.jpg
✅ IMG_002.jpg → trip_2.jpg
✅ IMG_003.jpg → trip_3.jpg

🎉 Rename completed successfully!

## 🤖 Author
[Your Name]  
💻 [Singh0622](https://github.com/Singh0622)  
📧 rahulsinghthakur0622@gmail.com