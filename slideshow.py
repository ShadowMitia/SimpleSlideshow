#! python

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

def copy_images(path_src, path_dst):
    for el in os.listdir(path_src):
        print(el)
        if el.split(".")[-1] in generate_page.authorized_extensions:
            src = os.path.join(path_src, el)
            dst = os.path.join(path_dst, el)
            copy(src, dst)
        else:
            dir_src = os.path.join(path_src, el)
			
def remove_images(path_src, path_dst):
    files = os.listdir(path_src)
    for el in os.listdir(path_dst):
        if el.split(".")[-1] in generate_page.authorized_extensions and el not in files:
            print("Removing " + el)
            os.remove(os.path.join(path_dst, el))

def main():
    print(path_to_drive)
    subprocess.Popen([chrome, "--kiosk", url_slideshow, "--incognito"])
    time.sleep(1)
    subprocess.Popen([firefox, url_concierge])
    remove_images(path_to_drive, "images")
    copy_images(path_to_drive, "images") # force copy images at startup

    while True:
        generate_page.main()
        time.sleep(5) # update every 30 minutes
        copy_images(path_to_drive, "images")
        remove_images(path_to_drive, "images")
		
if __name__ == '__main__':
    main()
