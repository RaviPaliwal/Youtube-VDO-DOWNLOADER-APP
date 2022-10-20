# import tkinter module
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
from tkinter import filedialog
import os
from pathlib import Path
import threading
global link
global name


root = Tk()
index = IntVar(root)
index.set(0)
cwd = str(Path.cwd())
img = PhotoImage(file=cwd+"\\ytlogo.png")
# Initialize tkinter window with dimensions
root.geometry('400x500')
root['background'] = '#947d43'
root.title("Youtube video Downloader")
root.wm_maxsize(width='460', height='500')
root.wm_minsize(width='460', height='500')


def showMsg(msg):
    messagebox.showinfo('Info', message=msg,)


def Download():
    try:
        def downloadstart(index):
            path = str(Path.home())
            yn = messagebox.askokcancel(
                "Continue Download", message=" Continue Download" + yt_video._title)
            if yn:
                resolutions[index].download(path+"//Downloads")
                showMsg('Download Successfull')
            else:
                showMsg("Cancelled")

        def start(index):
            try:
                index = IntVar()
                index = int(index_Tf.get())
                downloadstart(index)
            except:
                ValueError(), RuntimeError()

        link = linkget.get()
        yt_video = YouTube(link)
        resolutions1 = yt_video.streams.filter(file_extension='mp4')
        resolutions = resolutions1.order_by('resolution')
        res_list1 = []
        
        for stream in resolutions:
            res_list1.append(stream.resolution)
        
        res_list = list(enumerate(res_list1))
        showMsg(res_list)
        
        Label(root, text='Select Resolution', bg='#947d43',
              font=("Arial", 18)).place(y='200', x='130')
        
        index_Tf = Entry(root, font=15)
        index_Tf.bind('<Return>', start)
        index_Tf.place(x='50', y='250', height=40, width="360")
    except:
        RuntimeError()


# Main part
lbl = Label(root, text='Enter Link',
            font=("Cambria", 25,), bg="#947d43").place(y='30', x='150')

linkget = Entry(root, font=(12), bg="#e5e4e6", foreground="#160042")
linkget.place(x='50', y='120', height=45, width='360')

logo= Frame(root)
l1 = Label(logo,image=img,bg="#947d43")
l1.pack(anchor="center")
logo.pack(side= "bottom",pady=20)



try:
    try:
        btn = Button(root, text='Download', pady='10', padx='20', font=(
            "", 12), activebackground='#B2B880', bg='#358A73', command=threading.Thread(target=Download).start, height='1', width='7')
        btn.pack(side='bottom', pady='50', padx='80')
    except RuntimeError():
        showMsg("Wait dude")

except RuntimeError():
    print("Runtime Error")

lbl2 = Label(root, text='Developed by Ravi Paliwal', bg="#947d43", fg='#ffffff',
             font=("Cambria", 12,)).place(y='470', x='140')

root.mainloop()
