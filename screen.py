import os
import shutil
import colorama
import functools

using_getch = False

try:
    import msvcrt
    read = msvcrt.getch
except ImportError:
    try:
        import getch
        read = getch.getch
        using_getch = True
    except ImportError:
        print("Please install getch or run bank9000™ on windows.")
        exit(69)

colorama.init()  # Enables ANSI codes on windows, see <insert output>.
# To prevent output buffering, see <insert output>.
print = functools.partial(print, flush=True, end='')
width, height = shutil.get_terminal_size()
height -= 1  # one line for remains at the end for cursor


def clear():
    """Clears the screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def move(x=width - 1, y=height):
    """Moves the cursor to a position on the screen"""
    if x < 0:
        x += width + 1
    if y < 0:
        y += height + 1
    print("\033[{};{}H".format(y + 1, x + 1), end='')

