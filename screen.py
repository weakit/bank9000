import os
import functools
import shutil

print = functools.partial(print, flush=True)  # To prevent output buffering, see <insert output>.
width, height = shutil.get_terminal_size()
height -= 1  # one line for remains at the end for cursor


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':
    import time
    import borders
    print("screen clear test")
    time.sleep(1)
    clear()
    print("screen cleared.")
    time.sleep(1)
    clear()
    print("border detection tests")
    print("width: ", width, "height: ", height)
    time.sleep(1)
    print(borders.line_border(width, height))
    time.sleep(3)

    clear()  # clear on exit
