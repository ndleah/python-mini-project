import glob
import tkinter as tk
from tkinter import *
import vlc


def last(list):
    return list[-1]


def music_name():
    global my_music, music_number
    return last(my_music[music_number].split('/'))


def play_music():
    global music_number, my_music, player, instance
    to_play = my_music[music_number]
    media = instance.media_new(to_play)
    player.set_media(media)
    player.play()


def pause_music():
    player.pause()


def next_music():
    global music_number, my_music, music_label
    if music_number < len(my_music) - 1:
        music_number += 1
    music_label.config(text=str(music_name()))


def previous_music():
    global music_number, my_music, music_label
    if music_number > 0:
        music_number -= 1
    music_label.config(text=str(music_name()))


music_number = 0

window = Tk()
window.geometry('330x120')
window.resizable(False, False)
window.title('Mp3 Player')

instance = vlc.Instance()
player = instance.media_player_new()

my_music = glob.glob('/home/shitij_agrawal/Music/*.mp3')  # path to music folder

play_image = PhotoImage(file='images/play.png')
pause_image = PhotoImage(file='images/pause.png')
forward_image = PhotoImage(file='images/forward.png')
backward_image = PhotoImage(file='images/backward.png')
stop_image = PhotoImage(file='images/stop.png')

music_label = tk.Label(window, text=music_name())

play = tk.Button(window, image=play_image, command=play_music)
pause = tk.Button(window, image=pause_image, command=pause_music)
forward = tk.Button(window, image=forward_image, command=next_music)
backward = tk.Button(window, image=backward_image, command=previous_music)
stop = tk.Button(window, image=stop_image, command=lambda: sys.exit())

play.place(x=130, y=50)
pause.place(x=10, y=50)
forward.place(x=190, y=50)
backward.place(x=70, y=50)
stop.place(x=250, y=50)
music_label.place(x=10, y=0)

window.mainloop()
