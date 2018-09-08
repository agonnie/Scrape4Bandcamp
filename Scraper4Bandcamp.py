from Scraper import Scraper

print("  __                           _")
print(" (_   _ ._ _. ._   _  ._ |_|_ |_)  _. ._   _|  _  _. ._ _  ._")
print(" __) (_ | (_| |_) (/_ |    |  |_) (_| | | (_| (_ (_| | | | |_)")
print("              |                                            |")
print("                 Setting Everything Up.                     ")

with open("album_list.txt", "r") as album_list:
    S4B = Scraper("C:/Music")
    for album in album_list:
        S4B.download(album)
