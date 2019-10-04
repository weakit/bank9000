import screen
import colorama as cl
import texty as tx
import time
import random

sc = screen  # for ease in external usage


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
    screen.read()


def init():
    screen.print(screen.colorama.Fore.LIGHTYELLOW_EX)
    screen.clear()
    tx.size(screen.width, screen.height)


def startup():
    screen.clear()
    startup_screen = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la("Starting BMS."), -2)
    )
    screen.print(startup_screen)
    screen.move(17, -4)
    time.sleep(1)
    screen.clear()
    screen.print(tx.overlay(tx.border(), logo(), tx.ln(tx.la("Press enter to continue."), -2)))
    screen.move(28, -4)
    wait_for_enter()
    screen.clear()


def make_list(heading, options, highlight=None):
    h, g = 11, 3
    if len(options) > screen.height - 18:
        # TODO: trim options
        pass
    options = [' ' + x + ' ' * (67 - len(x)) for x in options]
    if highlight is not None:
        options[highlight] = cl.Fore.BLACK + cl.Back.LIGHTYELLOW_EX + options[highlight] + cl.Back.RESET + cl.Fore.LIGHTYELLOW_EX
    options = zip(options, range(h + g, h + g + len(options)))
    s = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la(heading, 4), h),
        tx.ln(tx.la('=' * 69), h + 1),
        *[tx.ln(tx.la(x[0]), x[1]) for x in list(options)]
    )
    return s


def list_handler(heading, options, go_back=False):
    choice = 0
    selected = False
    if go_back:
        options.append("Return to previous menu")
    while not selected:
        screen.clear()
        screen.print(make_list(heading, options, choice))
        screen.move(0, -1)
        key = ord(screen.read())
        if key == 13:  # enter
            selected = True
            if go_back and choice + 1 == len(options):
                return -1
            return choice
        elif key == 27:  # esc
            choice = -1
            selected = True
            return -1
        elif key == 224:  # special keys
            key = ord(screen.read())  # get second char
            if key == 72:  # arrow up
                choice = max(choice - 1, 0)
            elif key == 80:  # arrow down
                choice = min(choice + 1, len(options) - 1)
            elif key == 81:  # page down
                choice = len(options) - 1
            elif key == 73:  # page up
                choice = 0
    return -1


def simple_input(heading, prompt):
    h, g = 11, 3
    screen.clear()
    s = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la(heading, 4), h),
        tx.ln(tx.la('=' * 69), h + 1),
        tx.ln(tx.la(prompt, 4), h + g)
    )
    screen.print(s)
    screen.move(len(prompt) + 6, h + g)
    x = input()
    return x


def finish():
    screen.clear()
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
    time.sleep(2.5)
    screen.print(cl.Fore.RESET + cl.Back.RESET)
    screen.clear()
    screen.print("bank9000™\n")


def process_list(heading, thing):
    list_handler(heading, 'list')


def process(thing_type, heading, thing):
    if thing_type == 'list':
        process_list(heading, thing)
    return None


if __name__ == '__main__':
    pass
