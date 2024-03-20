import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from threading import Thread
from pathlib import Path
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import re
import sys

# import keyboard
# import shlex


class YoutubeDownloader:

    def __init__(self, root):
        def resource_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("640x642")
        root.minsize(420, 660)
        self.root.resizable(True, True)

        image_path = resource_path("icon.ico")
        root.iconbitmap(image_path)
        self.root.configure(background="#ffffff")

        # Define fonts
        heading_font = ("Arial", 22, "bold")
        captions_font = ("Arial",9)
        label_font = ("Arial", 11)
        button_font = ("Serif", 12, "bold")

        # Define colors
        bg_color = "#ffffff"
        fg_color = "#000000"
        accent_color = "#ff0000"
        button_bg_color = "#ff0000"
        button_fg_color = "white"

        # Set custom font for the heading
        heading_label = ttk.Label(root, text="YouTube Downloader", font=heading_font, background=bg_color, foreground=fg_color)
        heading_label.pack(pady=5)

        # Labels and Entry
        self.link_label = ttk.Label(root, text="Enter YouTube Video Link:", font=label_font, background=bg_color, foreground=fg_color)
        self.link_label.pack(pady=10)
        self.link_entry = ttk.Entry(root, width=60)
        self.link_entry.pack(pady=5)

        # Fetch Button
        self.fetch_button = ttk.Button(root, text="Fetch Video Info", command=self.start_fetching_info, style="Accent.TButton")
        self.fetch_button.pack(pady=5)

        # Thumbnail Label
        self.thumbnail_label = ttk.Label(root, text="Video Thumbnail Shows Here...", background=bg_color, foreground=fg_color)
        self.thumbnail_label.pack(pady=10)

        # Video Name Label
        self.video_name_label = ttk.Label(root, text="", background=bg_color, foreground=fg_color)
        self.video_name_label.pack(pady=5)

        # Type Label and Dropdown
        self.type_label = ttk.Label(root, text="Type:", font=label_font, background=bg_color, foreground=fg_color)
        self.type_label.pack(pady=5)
        self.type_var = tk.StringVar(value="Video")  # Set default type to "Video"
        self.type_dropdown = ttk.Combobox(root, textvariable=self.type_var, state="readonly", width=25)
        self.type_dropdown['values'] = ['Video', 'Audio']
        self.type_dropdown.pack(pady=5)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_quality_options)
         
        # Quality Label and Dropdown
        self.quality_label = ttk.Label(root, text="Select Quality:", font=label_font, background=bg_color, foreground=fg_color)
        self.quality_label.pack(pady=5)
        self.quality_var = tk.StringVar()
        self.quality_dropdown = ttk.Combobox(root, textvariable=self.quality_var, state="readonly", width=25)
        self.quality_dropdown.pack(pady=5)

        # Download Button
        self.download_button = ttk.Button(root, text="Download", command=self.start_download, style="Accent.TButton")
        self.download_button.pack(pady=10)
 
        # Info Label
        self.info_label = ttk.Label(root, text="Paste a Link to Download", font=captions_font, background=bg_color, foreground=fg_color)
        self.info_label.pack(pady=5)
        
        # Developer profile link
        self.developer_label = tk.Label(root, text="Developer Profile- Ravi Paliwal", font=label_font, background=bg_color, foreground=fg_color, cursor="hand2",justify="center")
        self.developer_label.pack(side="bottom", fill="x", padx=10, pady=25)
        self.developer_label.bind("<Button-1>", self.open_developer_profile)
   
        # Define custom style for buttons
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Accent.TButton", background=button_bg_color, foreground=button_fg_color, font=button_font)
        self.style.map("Accent.TButton", background=[("active", button_bg_color)])
        
        # Initialize video and audio quality options
        self.video_quality_options = []
        self.audio_quality_options = []

        # Register Ctrl+S hotkey to restart the application
        # keyboard.add_hotkey('ctrl+s', self.restart_application)

    def open_developer_profile(self, event):
        import webbrowser
        webbrowser.open("https://www.linkedin.com/posts/RaviPaliwal2003/")    

    def start_fetching_info(self):
        video_link = self.link_entry.get()
        if video_link:
            thread = Thread(target=self.fetch_video_info, args=(video_link,))
            thread.start()
        else:
            messagebox.showwarning("Warning", "Please enter a YouTube video link.")

    def fetch_video_info(self, video_link):
        try:
            # # Show fetching message
            # self.fetch_button.pack_forget()
            # self.info_label.config(text="Fetching video information...")
            # self.root.update()

            # Fetch video info
            yt = YouTube(video_link)
            thumbnail_url = yt.thumbnail_url
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                img_data = Image.open(BytesIO(response.content))
                img_data = img_data.resize((int(img_data.width / 2.5), int(img_data.height / 2.5)), Image.LANCZOS)
                thumbnail_image = ImageTk.PhotoImage(img_data)
                self.thumbnail_label.config(image=thumbnail_image)
                self.thumbnail_label.image = thumbnail_image
            else:
                self.thumbnail_label.config(text="Thumbnail not available")
            
            self.video_name_label.config(text="Video Name: " + yt.title)

            # Fetch video and audio quality options
            self.video_quality_options = [stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')]
            self.audio_quality_options = [stream.abr for stream in yt.streams.filter(only_audio=True)]
            self.update_quality_options()
            self.info_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch video info: " + str(e))
        finally:
            # Show the Fetch button again after fetching
            self.fetch_button.pack(pady=5)

    def update_quality_options(self, event=None):
        selected_type = self.type_var.get()
        if selected_type == 'Video':
            quality_options = self.video_quality_options
        else:
            quality_options = self.audio_quality_options
        
        self.quality_dropdown['values'] = quality_options
        if quality_options:
            self.quality_var.set(quality_options[0])
        else:
            self.quality_var.set("")

    def start_download(self):
        video_link = self.link_entry.get()
        quality = self.quality_var.get()
        if video_link:
            if quality:
                self.info_label.config(text="Downloading...")

                # Schedule the hiding and showing operations after a short delay
                self.root.after(100, self.hide_buttons)
                
                # Start the download in a separate thread
                thread = Thread(target=self.download_video, args=(video_link, quality))
                thread.start()
                
            else:
                messagebox.showwarning("Warning", "Please select a quality option.")
        else:
            messagebox.showwarning("Warning", "Please enter a YouTube video link.")

    def hide_buttons(self):
        self.download_button.pack_forget()
        self.developer_label.pack_forget()

    def show_buttons(self):
        self.download_button.pack(pady=10)
        self.developer_label.pack(side="bottom", fill="x", padx=10, pady=25)
        self.developer_label.bind("<Button-1>", self.open_developer_profile)

    def download_video(self, link, quality):
        try:
            yt = YouTube(link)
            if self.type_var.get() == 'Video':
                stream = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()
            else:
                stream = yt.streams.filter(only_audio=True, abr=quality).first()

            download_path = str(Path.home() / "Downloads/YoutubeDownloader/")
            if self.type_var.get() == 'Video':
                filename = stream.default_filename
            else:
                filename = f"{yt.title}.mp3"

            # Sanitize the filename
            filename = re.sub(r'[^\w\s.-]', '_', filename)

            # Check if the file already exists, if so, modify the filename
            i = 1
            while os.path.exists(os.path.join(download_path, filename)):
                if self.type_var.get() == 'Video':
                    filename = f"{stream.default_filename.split('.')[0]}_{i}.{stream.default_filename.split('.')[1]}"
                else:
                    filename = f"{yt.title}_{i}.mp3"
                i += 1

            # Download the file
            stream.download(download_path, filename=filename)

            self.info_label.config(text="Download completed successfully!")
        except Exception as e:
            self.info_label.config(text="Error: " + str(e))
            print("Error: " + str(e))
        finally:
            # self.download_button.config(state="normal")
            self.download_button.config(state="normal")
            self.quality_var.set("")
            self.show_buttons()

    # def restart_application(self):
    #     # Hardcoded path to the script
    #     script_path = '''C:/Users/"Ravi Paliwal"/Desktop/Exe's/YoutubeDownloader.py'''
    #     # Construct the command with proper quoting
    #     command = [sys.executable, script_path] + [shlex.quote(arg) for arg in sys.argv[1:]]
    #     # Execute the command
    #     os.execl(sys.executable, *command)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()

