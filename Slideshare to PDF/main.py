import io
import os
import sys
import pathlib
import tkinter as tk
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup
import PIL.Image
import validators

path = pathlib.Path().resolve()

def get_pdf(URL: str, info_label_2=None):
    if not URL or not validators.url(URL):
        msg = "Please provide a valid presentation link."
        if info_label_2:
            info_label_2.configure(text=msg)
        else:
            print(msg)
        return False

    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        msg = f"Connection error: {e}"
        if info_label_2:
            info_label_2.configure(text="Connection ERROR")
        else:
            print(msg)
        return False

    try:
        soup = BeautifulSoup(r.content, "html5lib")
    except Exception:
        soup = BeautifulSoup(r.content, "html.parser")

    imgs = soup.find_all("img", class_="slide-image")
    if not imgs:
        msg = "No slide images found on the provided page."
        if info_label_2:
            info_label_2.configure(text=msg)
        else:
            print(msg)
        return False

    img_src = []
    for x in imgs:
        srcset = x.get("srcset")
        if srcset:
            parts = srcset.split(",")
            if parts:
                src_link = parts[-1].strip().split(" ")[0].split("?")[0]
                img_src.append(src_link)
        elif x.get("src"):
            img_src.append(x.get("src").split("?")[0])

    if not img_src:
        msg = "Could not extract image source links."
        if info_label_2:
            info_label_2.configure(text=msg)
        return False

    imagesJPG = []
    for link in img_src:
        try:
            im = requests.get(link, timeout=10)
            f = io.BytesIO(im.content)
            imgJPG = PIL.Image.open(f)
            imagesJPG.append(imgJPG)
        except Exception:
            pass

    if not imagesJPG:
        msg = "Failed to download slide images."
        if info_label_2:
            info_label_2.configure(text=msg)
        else:
            print(msg)
        return False

    page_title = soup.title.string.strip() if (soup.title and soup.title.string) else "presentation"
    filename = f"{page_title}.pdf"

    try:
        imagesJPG[0].save(filename, save_all=True, append_images=imagesJPG[1:])
        msg = f"Downloaded to:\n{os.path.abspath(filename)}"
        if info_label_2:
            info_label_2.configure(text=msg)
        else:
            print(msg)
        return True
    except Exception as err:
        msg = f"Save Error: {err}"
        if info_label_2:
            info_label_2.configure(text=msg)
        return False

def run_gui():
    base = tk.Tk()
    base.geometry("350x320")
    base.title("Slideshare to PDF")
    base.resizable(False, False)
    base.configure(background="aliceblue")

    url_var = tk.StringVar()
    val_entry = tk.Entry(base, textvariable=url_var, width="35")
    val_entry.place(x=50, y=50)
    val_entry.focus_set()

    info_label_2 = tk.Label(base, text="", bg="aliceblue", fg="navy")
    info_label_2.place(x=35, y=230)

    button = tk.Button(base, text="Get PDF", command=lambda: get_pdf(url_var.get().strip(), info_label_2), width="25", height="2", bg="grey", fg="white")
    button.place(x=50, y=90)

    info_label = tk.Label(base, text="Enter presentation link.\nRequires active internet connection.", bg="aliceblue")
    info_label.place(x=35, y=160)

    base.mainloop()

def main():
    if len(sys.argv) > 1:
        get_pdf(sys.argv[1])
    else:
        run_gui()

if __name__ == '__main__':
    main()

