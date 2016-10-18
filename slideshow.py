# Script by Dimitri Belopopsky
# Requires https://github.com/ShadowMitia/SimpleSlideshow
# Put this script in the same folder as the SimpleSlideshow app

import time
import generate_page
import os
import subprocess
from shutil import copy

url_slideshow = os.path.abspath("index.html")
url_concierge = "http://concierge.la-faps.fr/week_all.php?area=1&pview=1"
chrome = os.path.join("C:\Program Files","Google","Chrome","Application","chrome.exe")
firefox = os.path.join("C:\Program Files","Mozilla Firefox","firefox.exe")
path_to_drive = os.path.join(os.path.expanduser("~"), "Google Drive", "Affiches")
# path_to_drive = os.path.join(os.path.expanduser("~"), "Dropbox", "images")

def copy_images(path_src, path_dst):
    for el in os.listdir(path_src):
        if el.split(".")[-1] in generate_page.authorized_extensions:
            src = os.path.join(path_src, el)
            dst = os.path.join(path_dst, el)
            copy(src, dst)
        else:
            dir_src = os.path.join(path_src, el)
            copy_images(dir_src, path_dst)

def main():
    print(url_slideshow)
    subprocess.Popen([chrome, "--kiosk", url_slideshow, "--incognito"])
    time.sleep(1)
    subprocess.Popen([chrome, "--kiosk", "--new-window", url_concierge, "--incognito"])
    copy_images(path_to_drive, "images") # force copy images at startup

    while True:
        generate_page.main()
        time.sleep(1800)  # update every 30 minutes
        copy_images(path_to_drive, "images")


if __name__ == '__main__':
    main()
