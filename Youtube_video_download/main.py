import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox

def download_video_cli(url: str, output_path: str = "."):
    try:
        from pytube import YouTube
    except ImportError:
        print("Error: 'pytube' is required. Install it via 'pip install pytube'.")
        return False

    if not url or not url.strip():
        print("Error: YouTube URL cannot be empty.")
        return False

    print(f"Fetching video info for: {url}")
    try:
        yt = YouTube(url.strip())
        stream = yt.streams.get_highest_resolution()
        if not stream:
            print("Error: No downloadable stream found.")
            return False

        os.makedirs(output_path, exist_ok=True)
        print(f"Downloading '{yt.title}'...")
        file_path = stream.download(output_path=output_path)
        print(f"Successfully downloaded to: {file_path}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def run_gui():
    root = tk.Tk()
    root.geometry('450x300')
    root.title("YouTube Video Downloader")
    root.configure(bg="#F0F0F0")

    tk.Label(root, text='YouTube Video Downloader', font=('Arial', 15, 'bold'), bg="#F0F0F0").pack(pady=10)

    link = tk.StringVar()

    tk.Label(root, text='Paste Link Here:', font=('Arial', 12, 'bold'), bg="#F0F0F0").pack(pady=5)
    link_enter = tk.Entry(root, width=50, textvariable=link, font=('Arial', 10))
    link_enter.pack(pady=5)
    link_enter.focus_set()

    status_label = tk.Label(root, text='', font=('Arial', 12), bg="#F0F0F0")
    status_label.pack(pady=10)

    def start_download_thread():
        url_text = link.get().strip()
        if not url_text:
            messagebox.showwarning("Input Error", "Please paste a YouTube URL before downloading.")
            return

        download_btn.config(state=tk.DISABLED)
        status_label.config(text="Downloading... Please wait.", fg="blue")

        def worker():
            try:
                from pytube import YouTube
                yt = YouTube(url_text)
                stream = yt.streams.get_highest_resolution()
                if stream:
                    stream.download()
                    root.after(0, lambda: status_label.config(text="Downloaded Successfully!", fg="green"))
                    root.after(0, lambda: messagebox.showinfo("Success", f"Video '{yt.title}' downloaded successfully!"))
                else:
                    root.after(0, lambda: status_label.config(text="Stream not found.", fg="red"))
            except Exception as e:
                root.after(0, lambda: status_label.config(text="Download Failed!", fg="red"))
                root.after(0, lambda: messagebox.showerror("Download Error", f"Failed to download video:\n{e}"))
            finally:
                root.after(0, lambda: download_btn.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()

    download_btn = tk.Button(root, text='Download', font=('Arial', 12, 'bold'),
                             bg="#4CAF50", fg="white", padx=10, pady=5, command=start_download_thread)
    download_btn.pack(pady=10)

    root.mainloop()

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        download_video_cli(url, out_dir)
    else:
        run_gui()

if __name__ == '__main__':
    main()

