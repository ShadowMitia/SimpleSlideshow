#! python

# Author: Dimitri Belopopsky

from time import sleep
import generate_page
import os
import subprocess
from shutil import copy
import platform
import argparse

def copy_image(file, list_files, path_dst):
    if file not in list_files and file.split(".")[-1] in generate_page.authorized_extensions:
        print("Adding " + file)
        dst = os.path.join(os.path.dirname(file), path_dst)
        copy(file, dst)
			
def remove_image(file, list_files, path_dst):
        if file.split(".")[-1] in generate_page.authorized_extensions and file not in list_files:
            print("Removing " + file)
            os.remove(os.path.join(path_dst, os.path.basename(file)))

def sync_images(file_list, destination_folder):
    for f in file_list:
        copy_image(f, file_list, destination_folder)
        remove_image(f, file_list, destination_folder)

def get_list_files(path_list):
    l =[]
    for el in path_list:
        for e in os.listdir(el):
            l.append(os.path.join(el, e))
    return l

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
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"images"))
    args = parser.parse_args()
    generate_page.img_folder = args.dest
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
    sync_images(get_list_files(args.folder), args.dest)
    generate_page.generate_page()

    # Open the webpage containing the slideshow
    # Firefox doesn't have a kiosk mode, so you need to add a plugin for it
    wb_process = subprocess.Popen([web_browser, os.path.join(os.path.dirname(os.path.abspath(__file__)),"index.html")])
    while True:
        time = len(args.folder) * (generate_page.speed + generate_page.transition)
        sleep(1800 if time < 1800 else time) # update every 30 minutes by default, longer if more images
        sync_images(get_list_files(args.folder), args.dest) # update images if new wb_process.terminate()
        generate_page.generate_page() # generate the new webpage

if __name__ == '__main__':
    main()
