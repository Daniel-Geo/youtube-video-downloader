# import the necessary modules
import sys
from pytubefix import YouTube
from moviepy import *
import os

# create two variables with two color values
R = '\033[1;31m'
W = '\033[0;0m'

# request the YouTube video link from the user
link = input("Enter the YouTube video link: ")

# creates a variable called yt and its value is the value of YouTube object

def progress_function(stream, chunk: bytes, bytes_remaining: int):
    file_size = stream.filesize
    current = ((file_size-bytes_remaining)/file_size)
    percent = ("{0:.1f}").format(current*100)
    progress = int(50*current)
    status = "█" * progress + "-" * (50-progress)
    sys.stdout.write(" ↳ |{bar}| {percent}%\r".format(bar=status, percent=percent))
    sys.stdout.flush()

yt = YouTube(link, on_progress_callback = progress_function)

title = yt.title.translate({ord(i): None for i in '/\\:*?\"<>|'})
# request the type of the required file from the user
typ = input("Enter the type of the file (video, audio): ")

# video file code
if typ == "video" or typ == "Video":
    extension = input("Enter the video extension (mp4, webm): ")
    if extension == "mp4" or extension == "webm":
        res = input("Enter the video resolution (144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p): ")
        if res == "360p":
            # create a variable named stream that has the value of the filtered streams in yt object in descending order
            stream = yt.streams.filter(file_extension=extension, res=res, progressive=True).order_by("resolution").desc().first()
        elif res == "144p" or res == "240p" or res == "480p" or res == "720p" or res == "1080p" or res == "1440p" or res == "2160p":
            stream = yt.streams.filter(file_extension=extension, res=res, progressive=False).order_by("resolution").desc().first()
        else:
            print(f"{R}Error \"{res}\" isn't the required response{W}")
            exit()
    else:
        print(f"{R}Error \"{extension}\" isn't the required response{W}")
        exit()

# audio file code
elif typ == "audio" or typ == "Audio":
    kbpm = input("Enter the audio bit rate (high, low): ")
    if kbpm == "High" or kbpm == "high" or kbpm == "H" or kbpm == "h":
        extension = "webm"
        stream = yt.streams.filter(type=typ.lower(), file_extension=extension).order_by("abr").desc().first()
    elif kbpm == "Low" or kbpm == "low" or kbpm == "L" or kbpm == "l":
        extension = "mp4"
        stream = yt.streams.filter(type=typ.lower(), file_extension=extension).order_by("abr").desc().first()
    else:
        print(f"{R}Error \"{kbpm}\" isn't the required response{W}")
        exit()

else:
    print(f"{R}Error \"{typ}\" isn't the required response{W}")
    exit()

try:
    # prints the estimated file size in megabytes
    print(f"The estimated file size is {stream.filesize_mb} MB")
except:
    None

if typ == "video" or typ == "Video":
    answer = input("Do you want to download the video? yes/no: ")
else:
    answer = input("Do you want to download the audio? yes/no: ")

if answer == "Yes" or answer == "yes" or answer == "Y" or answer == "y":
    if typ == "video" or typ == "Video":
        if res == "360p":
            try:
                stream.download()
            except:
                print("Sorry the video isn't available with these requirements😥")

        else:
            try:
                pre = "audio_"
                stream.download()
                yt.streams.filter(type="audio", file_extension="mp4").order_by("abr").desc().first().download(filename_prefix=pre)
                video = VideoFileClip(f"{title}.{extension}")
                audio = AudioFileClip(f"{pre}{title}.m4a")
                final_video = video.with_audio(audio)
                final_video.write_videofile(f"YVD {title}.{extension}")
                os.remove(f"{title}.{extension}")
                os.remove(f"{pre}{title}.m4a")
            except:
                print("Sorry the video isn't available with these requirements😥")
    else:
        try:
            stream.download()
            audio = AudioFileClip(f"{title}.m4a")
            if kbpm == "High" or kbpm == "high" or kbpm == "H" or kbpm == "h":
                audio.write_audiofile(f"YVD {title}.wav")
            else:
                audio.write_audiofile(f"YVD {title}.mp3")
            os.remove(f"{title}.m4a")
        except:
            print("Sorry the video isn't available with these requirements😥")

elif answer == "No" or answer == "no" or answer == "N" or answer == "n":
    exit()
else:
    print(f"{R}Error \"{answer}\" isn't the required response{W}")
    exit()
