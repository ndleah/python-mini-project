import os
import shutil

#  Customize your categories here
CATEGORIES = {
    "Documents": ["pdf", "docx", "txt", "csv", "xlsx", "pptx"],
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg"],
    "Videos": ["mp4", "mkv", "mov", "avi"],
    "Music": ["mp3", "wav", "flac", "aac"],
    "Archives": ["zip", "rar", "7z", "tar", "gz"],
    "Code": ["py", "js", "html", "css", "cpp", "java"],
    "Others": []  # fallback category for unlisted extensions
}

def get_category(extension):
    """Return the matching category for a given file extension."""
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def organize_files(folder_path):
    """Organize files by predefined categories."""
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isdir(file_path):
            continue  # skip directories

        # Get file extension
        ext = os.path.splitext(filename)[1].lower().strip('.')
        category = get_category(ext)

        # Create category folder
        target_dir = os.path.join(folder_path, category)
        os.makedirs(target_dir, exist_ok=True)

        # Move the file
        target_path = os.path.join(target_dir, filename)
        shutil.move(file_path, target_path)

        print(f"Moved: {filename} → {category}/")

    print("\nAll files organized successfully!")

if __name__ == "__main__":
    path = input("Enter the folder path to organize: ").strip()
    organize_files(path)
