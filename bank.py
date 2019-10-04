import screen
import colorama as cl
import texty as tx
import time
import random
from pynput import keyboard


def logo():
    typ = """\n
    ██████╗  █████╗ ███╗  ██╗██╗  ██╗  █████╗  ██████╗  ██████╗  ██████╗ TM
    ██╔══██╗██╔══██╗████╗ ██║██║ ██╔╝ ██╔══██╗██╔═████╗██╔═████╗██╔═████╗
    ██████╔╝███████║██╔██╗██║█████╔╝  ╚██████║██║██╔██║██║██╔██║██║██╔██║
    ██╔══██╗██╔══██║██║╚████║██╔═██╗   ╚═══██║████╔╝██║████╔╝██║████╔╝██║
    ██████╔╝██║  ██║██║ ╚███║██║  ██╗  █████╔╝╚██████╔╝╚██████╔╝╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚══╝╚═╝  ╚═╝  ╚════╝  ╚═════╝  ╚═════╝  ╚═════╝ 
    """
    slogans = [' ' * 46 + 'a bank you can trust',
               ' ' * 49 + 'the future, today']
    return typ + random.choice(slogans)


def wait_for_enter():
    with keyboard.Listener(on_press=lambda x: x is not keyboard.Key.enter) as listener:
        listener.join()


def init():
    screen.print(screen.colorama.Fore.LIGHTYELLOW_EX)
    screen.clear()
    tx.size(screen.width, screen.height)


def startup():
    startup_screen = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la("Starting BMS"), -2)
    )
    screen.print(startup_screen)
    screen.move(16, -4)
    time.sleep(1)
    screen.clear()
    screen.print(tx.overlay(tx.border(), logo(), tx.ln(tx.la("Press enter to continue."), -2)))
    screen.move(28, -4)
    wait_for_enter()
    screen.clear()


def make_list(heading, options, highlight=None):
    h, g = 11, 3
    if len(options) > screen.height - 18:
        # trim options
        pass
    options = [' ' + x + ' ' * (24 - len(x)) for x in options]
    if highlight is not None:
        options[highlight] = cl.Fore.BLACK + cl.Back.LIGHTYELLOW_EX + options[highlight] + cl.Back.RESET + cl.Fore.LIGHTYELLOW_EX
    options = zip(options, range(h + g, h + g + len(options)))
    s = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la(heading, 4), h),
        tx.ln(tx.la('=' * 69), h+1),
        *[tx.ln(tx.la(x[0]), x[1]) for x in list(options)]
    )
    return s


def list_handler(heading, options, go_back=False):
    choice = 0
    enter_pressed = False
    screen.clear()
    screen.print(make_list(heading, options, choice))
    screen.move(1, -1)

    def update(key):
        nonlocal choice, enter_pressed
        if key == keyboard.Key.enter:
            enter_pressed = True
            return False
        elif key == keyboard.Key.esc:
            choice = -1
            enter_pressed = True
            return False
        elif key == keyboard.Key.up:
            choice = max(choice - 1, 0)
        elif key == keyboard.Key.down:
            choice = min(choice + 1, len(options) - 1)
        elif key == keyboard.Key.page_down:
            choice = len(options) - 1
        elif key == keyboard.Key.page_up:
            choice = 0
        if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.page_up, keyboard.Key.page_down]:
            screen.clear()
            screen.print(make_list(heading, options, choice))
            screen.move(1, -1)

    while not enter_pressed:
        listener = keyboard.Listener(on_press=update)
        listener.start()
        listener.join()
    listener.stop()
    return choice


def finish():
    random.seed(time.time())
    backs = [cl.Back.MAGENTA,
             cl.Back.GREEN,
             cl.Back.RED,
             cl.Back.YELLOW,
             cl.Back.LIGHTRED_EX,
             cl.Back.LIGHTBLACK_EX,
             cl.Back.LIGHTGREEN_EX,
             cl.Back.LIGHTMAGENTA_EX,
             cl.Back.MAGENTA]
    screen.print(cl.Fore.BLACK + random.choice(backs) + tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la("Have a nice day!"), -2),
        tx.ln(tx.la("Thanks for using bank9000™."), -3)
    ))
    time.sleep(3)
    screen.print(cl.Fore.RESET + cl.Back.RESET)
    screen.clear()
    screen.print("bank9000™\n")


if __name__ == '__main__':
    init()
    # startup()
    #
    # finish()
    a = list_handler('Accounts', ['op1', 'op2', 'op3', 'op4'])
    print(a)
