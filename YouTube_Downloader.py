from __future__ import unicode_literals
from asyncio.windows_events import NULL
from tkinter.filedialog import askdirectory
#import youtube_dl
import yt_dlp as youtube_dl
import os
from sys import argv
import time
import shutil


# Download config
download_mp3 = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'nocheckcertificate': True,
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
}

download_mp4 = {
    "format":"bestvide[height<=1080]+bestaudio/best[height<=1080]",
    "outtmpl": "%(title)s.%(ext)s"
}


def download(link, download_options):
    with youtube_dl.YoutubeDL(download_options) as dl:
        try:
                dl.download([link])
        except:
                print("\n[!] Error downloading '"+link+"' ------------------------------------------------------")


def main(options):
        urls = []
        num = NULL

        # Get number of videos user wants to download
        while num == NULL:
            try:
                num = int(input("\n[?] How many videos are you going to download? >> "))
            except:
                print("    [!] Please enter a valid number!\n")

        # Open songs file and write urls as user inputs them
        with open("songs.txt", "w+") as txt:
            for i in range(num):
                url = input("[+] Paste Video URL "+str(i + 1)+" >> ")
                if "https://www.youtube.com/watch?v=" in url or "https://www.youtube.com/playlist?list=" in url:
                    txt.write(url + "\n")
                    urls.append(url)
                else:
                    if url != "":
                        print("   [!] Invalid URL entered")

        #check if valid songs have been input
        if not urls:
            print("\n    [!] No URLs Specified!")

        #checks to see if specified directory exists or not, if so, breaks
        dir_choice = NULL
        while dir_choice == NULL:
            print("\n[?] Enter location for downloads to be saved to:")
            print("    [+] Enter '1' for Desktop")
            print("    [+] Enter '2' for custom folder")
            dir_choice = input(" >> ")

            if dir_choice == "2":
                path = str(input("[+] Enter save path >> "))
                if os.path.isfile(path):
                    print("[!] Invalid path specified!")
                else:
                    if not os.path.exists(path):
                        try:
                            os.path.create(path)
                            print(f"    [+] Created path '{0}'", path)
                            dir_choice = path
                        except:
                            print("    [!] Failed to create path!")
                    else:
                        dir_choice = path
            elif dir_choice == "1":
                dir_choice = os.path.expanduser("~/Desktop/Downloads/")
            else:
                print("[!] Unknown input!")
        
        options["outtmpl"] = os.path.join(dir_choice, "%(title)s.%(ext)s")

        #Download confirmation  
        answer = input("\n[?] Start the download? (Yes/No) >> ")
        if answer.lower()[:1] == "n":
            return print("[!] Exiting Download")

        #download Songs
        print("[+] Starting Download...")
        for link in urls:
            download(link, options)

        print('\n\n[+] Successfully downloaded!')
        print('[+] Downloads have been saved in: '+dir_choice+"'.")



if __name__ == "__main__":
    while True:
        print("\n -+= Developed By EternalBlue#8132 =+-")
        print("[+] Type '1' to download YouTube Audio (MP3)")
        print("[+] Type '2' to download YouTube Videos (MP4)")
        p = str(input(" >> "))

        if p == "1" or p.lower() == "mp3" or p.lower() == "audio":
            main(download_mp3)
        elif p == "2" or p.lower() == "mp4" or p.lower() == "video":
            main(download_mp4)
        elif p.lower()[:1] == "e" or p.lower()[:1] == "q":
            exit()
        else:
            print("\n[!] Invalid choice! Type 'exit' or 'quit' to cancel.")