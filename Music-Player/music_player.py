import os
import sys
import glob
import tkinter as tk
from tkinter import filedialog, messagebox

def resolve_path(relative_path: str) -> str:
    """Resolve asset paths relative to the script directory."""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)

def get_default_music_files() -> list:
    """Search for MP3 files in script dir and user's default Music folder."""
    script_dir = os.path.dirname(__file__)
    files = glob.glob(os.path.join(script_dir, '*.mp3'))
    if files:
        return files

    user_music = os.path.expanduser('~/Music')
    if os.path.exists(user_music):
        files = glob.glob(os.path.join(user_music, '*.mp3'))
        if files:
            return files
    return []

def run_player():
    global my_music, music_number, player, instance, music_label

    music_number = 0
    my_music = get_default_music_files()

    window = tk.Tk()
    window.geometry('380x160')
    window.resizable(False, False)
    window.title('Mp3 Player')

    try:
        import vlc
        instance = vlc.Instance()
        player = instance.media_player_new()
    except Exception:
        instance = None
        player = None

    def get_current_track_name():
        if not my_music or music_number >= len(my_music):
            return "No Music Loaded"
        return os.path.basename(my_music[music_number])

    def play_music():
        global player, instance
        if not my_music:

            messagebox.showinfo("No Tracks", "Please select a folder with .mp3 files.")
            return
        if not player or not instance:
            messagebox.showerror("VLC Error", "VLC Python module ('python-vlc') or VLC media player library is not installed.")
            return

        to_play = my_music[music_number]
        media = instance.media_new(to_play)
        player.set_media(media)
        player.play()

    def pause_music():
        if player:
            player.pause()

    def next_music():
        global music_number
        if my_music and music_number < len(my_music) - 1:
            music_number += 1
            music_label.config(text=get_current_track_name())

    def previous_music():
        global music_number
        if my_music and music_number > 0:
            music_number -= 1
            music_label.config(text=get_current_track_name())

    def select_folder():
        global my_music, music_number
        chosen_dir = filedialog.askdirectory(title="Select Folder with MP3 Files")
        if chosen_dir:
            found = glob.glob(os.path.join(chosen_dir, '*.mp3'))
            if found:
                my_music = found
                music_number = 0
                music_label.config(text=get_current_track_name())
                messagebox.showinfo("Folder Loaded", f"Loaded {len(found)} track(s).")
            else:
                messagebox.showwarning("No MP3 Found", f"No .mp3 files found in '{chosen_dir}'.")

    # Load UI button icons safely
    play_img_path = resolve_path('images/play.png')
    pause_img_path = resolve_path('images/pause.png')
    forward_img_path = resolve_path('images/forward.png')
    backward_img_path = resolve_path('images/backward.png')
    stop_img_path = resolve_path('images/stop.png')

    try:
        play_image = tk.PhotoImage(file=play_img_path)
        pause_image = tk.PhotoImage(file=pause_img_path)
        forward_image = tk.PhotoImage(file=forward_img_path)
        backward_image = tk.PhotoImage(file=backward_img_path)
        stop_image = tk.PhotoImage(file=stop_img_path)
        has_icons = True
    except Exception:
        has_icons = False

    music_label = tk.Label(window, text=get_current_track_name(), font=("Arial", 10, "bold"), fg="darkblue")
    music_label.place(x=10, y=10)

    if has_icons:
        pause_btn = tk.Button(window, image=pause_image, command=pause_music)
        backward_btn = tk.Button(window, image=backward_image, command=previous_music)
        play_btn = tk.Button(window, image=play_image, command=play_music)
        forward_btn = tk.Button(window, image=forward_image, command=next_music)
        stop_btn = tk.Button(window, image=stop_image, command=window.destroy)
    else:
        pause_btn = tk.Button(window, text="Pause", command=pause_music, width=6)
        backward_btn = tk.Button(window, text="Prev", command=previous_music, width=6)
        play_btn = tk.Button(window, text="Play", command=play_music, width=6)
        forward_btn = tk.Button(window, text="Next", command=next_music, width=6)
        stop_btn = tk.Button(window, text="Exit", command=window.destroy, width=6)

    folder_btn = tk.Button(window, text="Browse Folder 📁", command=select_folder, font=("Arial", 9, "bold"))

    pause_btn.place(x=10, y=50)
    backward_btn.place(x=70, y=50)
    play_btn.place(x=130, y=50)
    forward_btn.place(x=190, y=50)
    stop_btn.place(x=250, y=50)
    folder_btn.place(x=10, y=110)

    window.mainloop()

def main():
    run_player()

if __name__ == '__main__':
    main()

