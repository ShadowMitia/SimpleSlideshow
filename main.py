import time
import generate_page


def main():

    while True:
        generate_page.main()
        time.sleep(3500)  # update every 5 minutes

if __name__ == '__main__':
    main()
