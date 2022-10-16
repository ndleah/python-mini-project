from tkinter import *
from pytube import YouTube

root = Tk()
root.geometry('450x300')
#root.resizable(0, 0)
root.title("Youtube Video Downloader")  # Title of the program

Label(root, text='Youtube Video Downloader',
      font='arial 15 bold').pack()  # Title of the program

link = StringVar()  # Variable for save link of video
filename = StringVar()  # Variable for save link of video

Label(root, text='Paste Link Here:', font='arial 13 bold').place(x=160, y=40)
link_enter = Entry(root, width=45, textvariable=link).place(
    x=50, y=90)  # Input for add the link

def Download():  # Function for download video

    Label(root, text='Downloading', font='arial 13').place(x=180, y=210)

    url = YouTube(str(link.get()))

    video = url.streams.get_highest_resolution()

    video.download()

    Label(root, text='Downloaded', font='arial 15').place(x=180, y=210)


Button(root, text='Download', font='arial 15 bold',
       padx=2, command=Download).place(x=180, y=150)

root.mainloop()
