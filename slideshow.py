#! python

# Main program file

import os
from os import path
import time
import shutil
import argparse

class PageGenerator:

    def __init__(self, images_folder, title = "SlideShow",
                 transition = 1000,
                 speed = 3500):
        self.title = title
        self.transition = transition
        self.speed = 3500
        self.images_folder = images_folder
        self.refresh_rate = len(images_folder) * (self.transition + self.speed)

    def _replace_tags(self, html_page, image_tags, num_tags):
        refresh_rate = num_tags * ((self.transition + self.speed) / 1000)
        refresh_rate = refresh_rate if refresh_rate > 0 else 30
        html_page = html_page.replace("{%title%}", self.title)
        html_page = html_page.replace("{%refresh-rate%}", str(refresh_rate))
        html_page = html_page.replace("{%slideshow%}", "true")
        html_page = html_page.replace("{%startOn%}", str(0))
        html_page = html_page.replace("{%speed%}", str(self.speed))
        html_page = html_page.replace("{%showNav%}", "false")
        html_page = html_page.replace("{%transition%}", str(self.transition))
        html_page = html_page.replace("{%images%}", image_tags)
        return html_page

    def _generate_img_tags(self, images):
        generate_tags = ""
        for img in images:
            generate_tags += "<img src='{}/{}' />\n".format(self.images_folder, img)
        return generate_tags

    def generate(self, images):
        tags = self._generate_img_tags(images)
        dir_path = path.dirname(self.images_folder)
        template_path = path.join(dir_path, "template.html")
        index_path    = path.join(dir_path, "index.html")
        with open(template_path, "r") as f, open(index_path, "w") as f2:
            html_template = f.read()
            html_page = self._replace_tags(html_template, tags, len(images))
            f2.write(html_page)


class ImageManager():

    def __init__(self, input_dirs, dest_dir):
        self.images = []
        self.input_dirs = []
        self.input_dirs_mtime = []
        for el in input_dirs:
            self.input_dirs.append(el)
            self.input_dirs_mtime.append(path.getmtime(el))
        self.dest_dir = dest_dir
        self.authorized_extensions = ["jpg", "jpeg", "tiff", "png", "bmp", "gif"]
        for el in self.input_dirs:
            self._get_remote_images(el)

    def sync_folders(self):

        def update_images(dir_path):
            self._get_remote_images(dir_path)
            return path.getmtime(dir_path)
        self.input_dirs_mtime = [update_images(self.input_dirs[i]) if path.getmtime(self.input_dirs[i]) > self.input_dirs_mtime[i] else self.input_dirs_mtime[i] for i in range(len(self.input_dirs)) ]
        self._remove_local_images()

    def _get_remote_images(self, path):
        img_list = os.listdir(path)
        for el in img_list:
            if self._is_valid_image(el) and el not in self.images:
                print("Adding: " + el)
                self.images.append(el)
                shutil.copy(os.path.join(path, el), self.dest_dir)
        for el in self.images:
            if el not in img_list:
                self.images.remove(el)

    def _remove_local_images(self):
        img_list = os.listdir(self.dest_dir)
        for el in img_list:
            if el not in self.images:
                print("Removing: " + el)
                os.remove(path.join(self.dest_dir, el))

    def _is_valid_image(self, img):
        return img.split(".")[-1] in self.authorized_extensions


class SlideshowManager:

    def __init__(self):
        self.argument_parser = argparse.ArgumentParser(description="Simple Slideshow")
        self.argument_parser.add_argument('-f',
                                     '--folder',
                                     metavar=('input_folder_paths'),
                                     type=str,
                                     help="path to folder with images to show",
                                     action="append",
                                     required=True)
        self.argument_parser.add_argument('-d',
                                     '--dest',
                                     metavar=('destination_folder'),
                                     type=str,
                                     help="path to destination folder where images are stored (default is 'images'",
                                     default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"images"))
        self.input_args = self.argument_parser.parse_args()

    def run(self):

        images_manager = ImageManager(self.input_args.folder, self.input_args.dest)
        images_manager.sync_folders()

        generator = PageGenerator(self.input_args.dest, "MaPS Slideshow")
        while True:
            images_manager.sync_folders()
            generator.generate(images_manager.images)
            time.sleep(60 * 5) # Update roughly every 5 minutes


if __name__ == '__main__':
    slideshow = SlideshowManager()
    slideshow.run()
