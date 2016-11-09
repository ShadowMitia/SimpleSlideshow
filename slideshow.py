#! python

# Author: Dimitri Belopopsky

from time import sleep
import generate_page
import os
import subprocess
from shutil import copy
import platform
import argparse

#path_to_drive = os.path.join(os.path.expanduser("~"), "Google Drive", "Conseil MAPS", "Affichage accueil")
#path_to_other = os.path.join(os.path.expanduser("~"), "Google Drive", "Affiches")

def copy_images(path_src, path_dst):
    files = os.listdir(path_dst)
    for el in os.listdir(path_src):
        if el not in files and el.split(".")[-1] in generate_page.authorized_extensions:
            src = os.path.join(path_src, el)
            dst = os.path.join(path_dst, el)
            copy(src, dst)
        else:
            dir_src = os.path.join(path_src, el)
			
def remove_images(path_src, path_dst):
    files = os.listdir(path_src)
    for el in os.listdir(path_dst):
        if el.split(".")[-1] in generate_page.authorized_extensions and el not in files:
            os.remove(os.path.join(path_dst, el))

def sync_images(folders, destination_folder):
    for f in folders:
        copy_images(f, destination_folder)
        remove_images(f, destination_folder)

def main():

    # parse input parameters
    parser = argparse.ArgumentParser(description="Simple Slideshow")
    parser.add_argument('-f',
                        '--folder',
                        metavar=('folder_path'),
                        type=str,
                        help="path to folder with images to show",
                        action="append",
                        required=True)
    parser.add_argument('-d',
                        '--dest',
                        metavar=('destination_folder'),
                        type=str,
                        help="path to destination folder where images are stored",
                        default="images")
    args = parser.parse_args()

    # grab firefox browser depending of system
    # NOT FULLY TESTED
    web_browser = ""
    if platform.system() in ["Linux", "Darwin"]:
        web_browser = "firefox"
    else:
        web_browser = os.path.join("C:\Program Files","Mozilla Firefox","firefox.exe")

    # Grab the images if there are new ones, and update webpage
    # This is useful when
    # 1) Starting for the first time this system
    # 2) If the slideshow has stopped for more than the refresh
    sync_images(args.folder, args.dest)
    generate_page.generate_page()

    # Open the webpage containing the slideshow
    # Firefox doesn't have a kiosk mode, so you need to add a plugin for it
    wb_process = subprocess.Popen([web_browser, "index.html"])
    while True:
        time = len(args.folder) * (generate_page.speed + generate_page.transition)
        sleep(1800 if time < 1800 else time) # update every 30 minutes by default, longer if more images
        sync_images(args.folder, args.dest) # update images if new wb_process.terminate()
        generate_page.generate_page() # generate the new webpage

if __name__ == '__main__':
    main()
