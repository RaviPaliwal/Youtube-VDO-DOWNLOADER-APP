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
# Initialize tkinter window with dimensions
root.geometry('400x500')
root['background'] = '#344b59'
root.title("Youtube video Downloader")
root.wm_maxsize(width='460', height='500')
root.wm_minsize(width='460', height='500')

def showMsg(msg):
    messagebox.showinfo('Message', message=msg,)

def Download():
    try:
        def downloadstart(index):
            path = str(Path.home())      
            showMsg(" Continue Download" +yt_video._title)
            resolutions[index].download(path+"//Downloads")
            showMsg('Download Successfull')
    
        def start(index):
            try:
                index= IntVar()
                index = int(index_Tf.get())
                downloadstart(index)
            except:ValueError()    
       
        link = linkget.get()
        yt_video = YouTube(link)
        resolutions1 = yt_video.streams.filter(file_extension='mp4')
        resolutions = resolutions1.order_by('resolution')
        res_list1= []
        for stream in resolutions:
            res_list1.append(stream.resolution)
        res_list = list(enumerate(res_list1))
        showMsg(res_list)
        Label(root, text='Select Resolution',bg='#344b59',font=("Arial", 15)).place(y='200',x='128')
        index_Tf = Entry(root)
        index_Tf.bind('<Return>',start)
        index_Tf.place(x='50', y='250',height=40,width='360')
    except:RuntimeError()
#Main part
lbl = Label(root, text='Enter Link',bg='#344b59',
            font=("Cambria",20,)).place(y='50',x='160')

linkget = Entry(root,font=(12))
linkget.place(x='50', y='120',height=40,width='360')
try:
    btn = Button(root, text='Download', pady='10', padx='20', font=(
        "", 12), activebackground='#B2B880', bg='#358A73',command=threading.Thread(target=Download).start,height='1',width='7')
    btn.pack(side='bottom', pady='50',padx='80')
except:RuntimeError()

lbl2= Label(root, text='Developed by Ravi Paliwal',bg='#344b59',fg='#ffffff',
            font=("Cambria",10,)).place(y='478',x='300')


root.mainloop()
# https://www.youtube.com/watch?v=CGTPdm4xX2o
