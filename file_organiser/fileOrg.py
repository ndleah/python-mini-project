import os
parent_dir = "E:/5.Python/fileorginaser/desktoptemp/"
direcO = "Others"
patho = os.path.join(parent_dir,direcO)
try:  
    os.mkdir(patho) 
except OSError as error:  
    print(error)


file_extension = {
    "aep": "AfterEffects",
    "psb": "Photoshop",
    "psd": "Photoshop",
    "pdf": "PDFs",
    "png": "Images",
    "jpg": "Images",
    "gif": "Images",
    "bmp": "Images",
    "txt": "Text Files",
    "docx": "Documents",
    "xlsx": "Data",
    "pptx": "Documents",
    "mp3": "Music",
    "mp4": "Videos",
    "avi": "Videos",
    "zip": "Archives",
    "rar": "Archives",
    "tar": "Archives",
    "exe": "Executable Files",
    "dll": "Dynamic Link Libraries",
    "html": "Code",
    "css": "Code",
    "js": "Code",
    "json": "Code",
    "xml": "Data",
    "sql": "Data",
    "py": "Code",
    "java": "Code",
    "cpp": "Code",
    "c": "Code",
    "h": "Code",
    "php": "Code",
    "asp": "Code",
    "bat": "Code",
    "cmd": "Code",
    "ini": "INI Configuration Files",
    "log": "Log Files",
    "cfg": "Configuration Files",
    "bak": "Backup Files",
    "tmp": "Temporary Files",
    "csv": "Data",
    "dat": "Data",
    "md": "Code",
    "url": "Shortcuts",
    "desktop": "Shortcuts",
    "lnk": "Links",
    "ics": "Others",
    "doc": "Documents",
}



dir_list = os.listdir(parent_dir)
folders = [item for item in dir_list if os.path.isdir(os.path.join(parent_dir, item))]
print(folders)
count = 0
for filename in dir_list:
    if filename in folders:
        continue
    ot = 0
    for ex in file_extension:
        if filename.endswith(ex):
            path = os.path.join(parent_dir,file_extension[ex])
            try:  
                os.mkdir(path)  
            except OSError as error:  
                print(error)
            oldpath=os.path.join(parent_dir,filename)
            newpath=os.path.join(path,filename)
            try: 
                os.rename(oldpath, newpath)
            except OSError as endswith:
                print(error)
            ot = 1
            count = count + 1
    if ot == 0:
        oldpath=os.path.join(parent_dir,filename)
        newpath=os.path.join(patho,filename)
        try: 
            os.rename(oldpath, newpath)
        except OSError as endswith:
            print(error)
print(f"Count: {count}")
    

