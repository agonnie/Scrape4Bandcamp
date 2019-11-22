from Source.Scraper import Scraper
from json.decoder import JSONDecodeError
print("  __                           _")
print(" (_   _ ._ _. ._   _  ._ |_|_ |_)  _. ._   _|  _  _. ._ _  ._")
print(" __) (_ | (_| |_) (/_ |    |  |_) (_| | | (_| (_ (_| | | | |_)")
print("              |                                            |")
print("                 Setting Everything Up.                     ")

with open("album_list.txt", "r") as album_list:
    S4B = Scraper("C:/Music")
    for album in album_list:
        try:
            S4B.download(album)
        except JSONDecodeError as e:
            print("Bad JSON for this album, cannot be downloaded.%s line:%s char:%s" % (e.msg, e.lineno, e.colno))
            input("Press any key to continue to next album")
        except Exception as e:
            print(type(e).__name__, "Bad JSON for this album, cannot be downloaded.")
            input("Press any key to continue to next album")
