import os

# transition between slides (milliseconds)
transition = 1000
# duration of each slide (milliseconds)
speed = 3500
# have the slideshow on or off(should stay true)
slide_show = True
# slideshow arrows on or off
show_nav = False
# which slide to start on
start_on = 0
# folder with images
img_folder = "images"
# title for the page
title = "Slideshow MaPS"
# authorised image formats
# should only be images that can be rendered in a navigator
authorized_extensions = ["jpg", "jpeg", "tiff", "png", "bmp", "gif"]


# pass in the image names, construct the proper html <img> sequence
def generate_img_html(images):
    imgs = ""
    for i in images:
        imgs += "<img src=\"images/{}\" alt=\"\" />\n".format(i)
    return imgs


# replace the tags in the template with the proper values
def replace_tags(html_page, html_images):
    html_page = html_page.replace("{%title%}", title)
    html_page = html_page.replace("{%slideshow%}",
                                  "true" if slide_show else "false")
    html_page = html_page.replace("{%startOn%}", str(start_on))
    html_page = html_page.replace("{%speed%}", str(speed))
    html_page = html_page.replace("{%showNav%}",
                                  "true" if show_nav else "false")
    html_page = html_page.replace("{%transition%}", str(transition))
    html_page = html_page.replace("{%images%}", html_images)

    return html_page


# here be all the magic
def main():
    directory_list = os.listdir(img_folder)
    images = []
    for entry in directory_list:
        if entry.split(".")[-1] in authorized_extensions:
            images.append(entry)

    html_images = generate_img_html(images)

    html_page = ""
    with open("template.html", "r") as f:
        html_page = f.read()

    html_page = replace_tags(html_page, html_images)

    with open("index.html", "w") as f:
        f.write(html_page)

if __name__ == '__main__':
    main()
