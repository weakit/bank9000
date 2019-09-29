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
    import texty as t
    import logos
    t.size(width, height)
    print("screen clear test")
    time.sleep(1)
    clear()
    print("screen cleared.")
    time.sleep(1)
    clear()
    print("border detection tests")
    print("width: ", width, "height: ", height)
    time.sleep(1)
    print(t.overlay(t.line_border(), t.centre_text("\nHello world."), t.centre_text("\n\n" + logos.screen)), end='')
    time.sleep(3)
    clear()
    print(t.overlay(t.line_border(), t.line_border(20, 10), t.line_border(10, 20)), end='')
    time.sleep(1)
    clear()  # clear on exit
