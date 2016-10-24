# Script by Dimitri Belopopsky
# Requires this: https://github.com/ShadowMitia/SimpleSlideshow
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

def copy_files():
    list_dir = os.listdir(path_to_drive)
    print(list_dir)
    for el in list_dir:
        el = os.path.join(path_to_drive, el)
        if os.path.isfile(el):
            if el.split(".")[-1] in generate_page.authorized_extensions:
                print(el)
                src = os.path.join(path_to_drive, el)
                dst = os.path.join("images", el)
                copy(src, dst)

def main():
    subprocess.Popen([chrome, "--kiosk", url_slideshow, "--incognito"])
    time.sleep(1)
    subprocess.Popen([chrome, "--kiosk", "--new-window", url_concierge, "--incognito"])
    copy_files()
    
    while True:
        generate_page.main()
        time.sleep(1800)  # update every 30 minutes
        copy_files
                
if __name__ == '__main__':
    main()
