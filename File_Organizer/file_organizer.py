import os       # for working with files and folders
import shutil   # for moving files
import sys      # for reading command line arguments
import json     # for saving/loading the undo log

# each key is a folder name, and the value is a list of
# file extensions that belong in that folder
categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".json"],
    "Executables": [".exe", ".msi", ".bat", ".sh"],
}


def get_category(extension):
    """check which category a file extension belongs to"""
    for folder_name, ext_list in categories.items():
        if extension.lower() in ext_list:
            return folder_name
    # if extension doesn't match anything, put it in "Others"
    return "Others"


def organize(folder_path):
    """sort all files in a folder into subfolders by type"""

    folder_path = os.path.abspath(folder_path)

    # make sure the folder actually exists
    if not os.path.isdir(folder_path):
        print("Error: '" + folder_path + "' is not a valid folder.")
        return

    print("\nOrganizing: " + folder_path + "\n")

    # go through each item in the folder
    move_log = []  # keep track of what we moved (for undo)
    count = {}     # count how many files per category

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # skip if it's a folder, hidden file, or this script itself
        if os.path.isdir(file_path):
            continue
        if filename.startswith("."):
            continue
        if filename == os.path.basename(__file__):
            continue

        # get the file extension (like ".pdf" or ".jpg")
        name, ext = os.path.splitext(filename)

        # figure out which category this file belongs to
        category = get_category(ext)

        # create the category folder if it doesn't exist yet
        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # build the destination path
        destination = os.path.join(category_folder, filename)

        # if a file with the same name already exists, add a number
        # example: photo.jpg becomes photo_1.jpg, photo_2.jpg, etc.
        if os.path.exists(destination):
            i = 1
            while os.path.exists(destination):
                destination = os.path.join(category_folder, name + "_" + str(i) + ext)
                i += 1

        # move the file
        shutil.move(file_path, destination)

        # log it and update the count
        move_log.append({"from": file_path, "to": destination})
        count[category] = count.get(category, 0) + 1
        print("  " + filename + " -> " + category + "/")

    # if nothing was moved
    if not move_log:
        print("No files to organize!")
        return

    # save a log file so we can undo later
    log_path = os.path.join(folder_path, ".organizer_log.json")
    with open(log_path, "w") as f:
        json.dump(move_log, f, indent=2)

    # print a summary
    total = sum(count.values())
    print("\nDone! Moved " + str(total) + " files.\n")
    for cat in sorted(count):
        print("  " + cat + ": " + str(count[cat]))
    print("\nTip: run with --undo to put everything back.")


def undo(folder_path):
    """move all organized files back to where they were"""

    folder_path = os.path.abspath(folder_path)
    log_path = os.path.join(folder_path, ".organizer_log.json")

    # check if the log file exists
    if not os.path.exists(log_path):
        print("Nothing to undo.")
        return

    # read the log
    with open(log_path, "r") as f:
        move_log = json.load(f)

    print("\nUndoing...\n")

    restored = 0
    for entry in move_log:
        if os.path.exists(entry["to"]):
            shutil.move(entry["to"], entry["from"])
            print("  Restored: " + os.path.basename(entry["from"]))
            restored += 1

    # clean up empty folders that were created
    all_categories = list(categories.keys()) + ["Others"]
    for cat in all_categories:
        cat_folder = os.path.join(folder_path, cat)
        if os.path.isdir(cat_folder) and len(os.listdir(cat_folder)) == 0:
            os.rmdir(cat_folder)

    # remove the log file
    os.remove(log_path)

    print("\nRestored " + str(restored) + " files.")


# --- main program starts here ---

if __name__ == "__main__":

    # check what the user typed in the command line
    if len(sys.argv) > 1 and sys.argv[1] == "--undo":
        # user wants to undo
        folder = sys.argv[2] if len(sys.argv) > 2 else "."
        undo(folder)

    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        # show help
        print("File Organizer - sorts files into folders by type")
        print("")
        print("Usage:")
        print("  python file_organizer.py              # organize current folder")
        print("  python file_organizer.py /some/path    # organize a specific folder")
        print("  python file_organizer.py --undo        # undo last organize")

    else:
        # organize the given folder (or current folder if none given)
        folder = sys.argv[1] if len(sys.argv) > 1 else "."
        organize(folder)
