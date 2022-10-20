from pytube import YouTube, Playlist


def youtube_video():
    link = input("Enter Playlist URL: ")
    print("\n\n")
    yt_video = YouTube(link)
    resolutions = yt_video.streams
    res_list = list(enumerate(resolutions))
    for i in res_list:
        {
            print(i)
        }
    print("\n")
    select_res = int(input("ENTER RESOLUTION CHOICE: "))
    print("Downloading " + yt_video._title)
    resolutions[select_res].download("C:\\Users\\Ravi Paliwal\\Downloads")
    print("Download Successfull")


def youtube_playlist():
    link = input("Enter Playlist URL: ")
    playlist = Playlist(link)
    resolutions = playlist.
    res_list = list(enumerate(resolutions))
    for i in res_list:
      print(i)
    print("\n")
    print("No of Videos in Playlist: %s" %len(playlist.video_urls))
       
      

print("Youtube Download Tools\n")
print("Select Task From Below\n 1.Video Download\n 2.Playlist Download")
Task = int(input())
if (Task == 1):
    # https://www.youtube.com/watch?v=CGTPdm4xX2o
    youtube_video()

elif (Task == 2):
    youtube_playlist()
