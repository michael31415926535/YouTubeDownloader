import yt_dlp as youtube_dl
from os import path, makedirs

download_mp3 = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'continuedl': True,
    'download_archive': 'archive.txt',
    'nooverwrites': True,
    'noprogress': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

download_mp4 = {
    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    'outtmpl': '%(title)s.%(ext)s',
    'ignoreerrors': True,
    'continuedl': True,
    'download_archive': 'archive.txt',
    'nooverwrites': True,
    'noprogress': False,
}


def hook_download_status(d):
    if d['status'] == 'finished':
        print(f"[+] Finished downloading: {d.get('filename', 'unknown file')}")
    elif d['status'] == 'error':
        print(f"[!] Failed to download: {d.get('filename', 'unknown file')}")
        with open("failed.txt", "a", encoding="utf-8") as f:
            f.write(f"{d.get('info_dict', {}).get('webpage_url', 'unknown')}\n")


def download(link, download_options):
    download_options.update({'progress_hooks': [hook_download_status]})
    with youtube_dl.YoutubeDL(download_options) as dl:
        try:
            dl.download([link])
        except Exception as e:
            print(f"[!] Error downloading '{link}': {e}")
            with open("failed.txt", "a", encoding="utf-8") as f:
                f.write(f"{link}\n")


def main(options):
    urls = []
    num = None

    while num is None:
        try:
            num = int(input("\n[?] How many videos are you going to download? >> "))
        except:
            print("    [!] Please enter a valid number!\n")

    with open("songs.txt", "w+", encoding="utf-8") as txt:
        for i in range(num):
            url = input("[+] Paste Video URL " + str(i + 1) + " >> ")
            if "https://www.youtube.com/watch?v=" in url or "https://www.youtube.com/playlist?list=" in url:
                txt.write(url + "\n")
                urls.append(url)
            elif url != "":
                print("  [!] Invalid URL entered")

    if not urls:
        print("\n    [!] No URLs Specified!")
        return

    dir_choice = None
    while dir_choice is None:
        print("\n[?] Enter location for downloads to be saved to:")
        print("    [+] Enter '1' for desktop")
        print("    [+] Enter '2' for custom folder")
        dir_choice = input(" >> ")

        if dir_choice == "2":
            folderPath = str(input("[+] Enter save path >> "))
            if path.isfile(folderPath):
                print("[!] Invalid path specified!")
                dir_choice = None
            else:
                if not path.exists(folderPath):
                    try:
                        makedirs(folderPath)
                        print(f"    [+] Created path '{folderPath}'")
                        dir_choice = folderPath
                    except:
                        print("    [!] Failed to create path!")
                        dir_choice = None
                else:
                    dir_choice = folderPath
        elif dir_choice == "1":
            dir_choice = path.expanduser("~/Desktop/Downloads/")
            if not path.exists(dir_choice):
                makedirs(dir_choice)
        else:
            print("[!] Unknown input!")
            dir_choice = None

    options["outtmpl"] = path.join(dir_choice, "%(title)s.%(ext)s")

    answer = input("\n[?] Start the download? (Yes/No) >> ")
    if answer.lower()[:1] == "n":
        print("[!] Exiting Download")
        return

    print("[+] Starting Download...")
    for link in urls:
        download(link, options)

    print('\n[+] Download process complete.')
    print(f'[+] Downloads saved in: {dir_choice}')
    print('[+] Failed URLs (if any) have been saved to failed.txt.')


if __name__ == "__main__":
    while True:
        print("\n -+= Developed By EternalBlue#8132 =+-")
        print("[+] Type '1' to download YouTube Audio (MP3)")
        print("[+] Type '2' to download YouTube Videos (MP4)")
        p = str(input(" >> "))

        if p == "1" or p.lower() in ["mp3", "audio"]:
            main(download_mp3)
        elif p == "2" or p.lower() in ["mp4", "video"]:
            main(download_mp4)
        elif p.lower()[:1] in ["e", "q"]:
            exit()
        else:
            print("\n[!] Invalid choice! Type 'exit' or 'quit' to cancel.")