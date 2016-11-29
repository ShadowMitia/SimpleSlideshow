#! python

# Author: Dimitri Belopopsky

from time import sleep
import generate_page
import os
import subprocess
from shutil import copy
import platform
import argparse

def copy_image(f, list_files, path_dst):
    if f not in list_files and f.split(".")[-1] in generate_page.authorized_extensions:
        print("Adding " + f)
        dst = os.path.join(os.path.dirname(f), path_dst)
        copy(f, dst)
			
def remove_image(f, list_files, path_dst):
        if f.split(".")[-1] in generate_page.authorized_extensions and f not in list_files:
            print("Removing " + f)
            os.remove(os.path.join(path_dst, os.path.basename(f)))

def sync_images(file_list, destination_folder):
    for f in file_list:
        copy_image(f, os.listdir(destination_folder), destination_folder)
        remove_image(f, os.listdir(destination_folder), destination_folder)

def get_list_files(path_list):
    return [os.path.join(el, e) for el in path_list for e in os.listdir(el)]


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
    generate_page.img_folder =  args.dest
    # grab firefox browser depending of system
    # NOT FULLY TESTED
    web_browser = ""
    if platform.system() in ["Linux", "Darwin"]:
        web_browser = "firefox"
    else:
        web_browser = os.path.join("C:\Program Files","Mozilla Firefox","firefox.exe")

    # Grab the images if there are new ones, and update webpage at least once before start
    files = get_list_files(args.folder)
    print(files)
    sync_images(files, args.dest)
    generate_page.generate_page()

    # Open the webpage containing the slideshow
    # Firefox doesn't have a kiosk mode, so you need to add a plugin for it
    wb_process = subprocess.Popen([web_browser, os.path.join(os.path.dirname(os.path.abspath(__file__)),"index.html")])
    while True:
        time = 1800  # update every 30 minutes by default, longer if more images
        new_time = len(args.folder) * (generate_page.speed + generate_page.transition)
        if new_time > time:
            time = new_time
        sleep(time)
        sync_images(get_list_files(args.folder), args.dest) # update images if new wb_process.terminate()
        generate_page.generate_page() # generate the new webpage

if __name__ == '__main__':
    main()
