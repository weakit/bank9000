import os
import functools
import shutil
import colorama

colorama.init()  # Enables ANSI codes on windows, see <insert output>.
print = functools.partial(print, flush=True, end='')  # To prevent output buffering, see <insert output>.
width, height = shutil.get_terminal_size()
height -= 1  # one line for remains at the end for cursor


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def move(x=width - 1, y=height):
    if x < 0:
        x += width + 1
    if y < 0:
        y += height + 1
    print("\033[{};{}H".format(y + 1, x + 1), end='')


if __name__ == '__main__':
    import time
    import texty as t
    t.size(width, height)
    print("screen clear test")
    time.sleep(1)
    clear()
    print(colorama.Fore.LIGHTGREEN_EX + "screen cleared." + colorama.Fore.RESET)
    time.sleep(1)
    clear()
    print("border detection tests")
    print("width: ", width, "height: ", height)
    time.sleep(1)
    clear()
    print(t.overlay(t.border(), t.ca("\nHello world."), t.ca("\n\n" + 'logos.screen')), end='')
    move()
    time.sleep(3)
    clear()
    print(t.overlay(t.border(), t.border(20, 10), t.border(10, 20)), end='')
    move()
    time.sleep(1)
    clear()  # clear on exit
