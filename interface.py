import screen
import colorama as cl
import texty as tx
import time
import random

sc = screen  # for ease in external usage


def logo():
    """Returns logo with a random slogan"""
    typ = """\n
    ██████╗  █████╗ ███╗  ██╗██╗  ██╗  █████╗  ██████╗  ██████╗  ██████╗ TM
    ██╔══██╗██╔══██╗████╗ ██║██║ ██╔╝ ██╔══██╗██╔═████╗██╔═████╗██╔═████╗
    ██████╔╝███████║██╔██╗██║█████╔╝  ╚██████║██║██╔██║██║██╔██║██║██╔██║
    ██╔══██╗██╔══██║██║╚████║██╔═██╗   ╚═══██║████╔╝██║████╔╝██║████╔╝██║
    ██████╔╝██║  ██║██║ ╚███║██║  ██╗  █████╔╝╚██████╔╝╚██████╔╝╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚══╝╚═╝  ╚═╝  ╚════╝  ╚═════╝  ╚═════╝  ╚═════╝ 
    """
    slogans = [' ' * 46 + 'a bank you can trust',
               ' ' * 49 + 'the future, today',
               ' ' * 42 + "we don't cheat sometimes",
               ' ' * 57 + 'open 24/7']
    return typ + random.choice(slogans)


def wait_for_key():
    """Waits for user keypress"""
    screen.read()


def init():
    """Initialize screen"""
    screen.print(screen.colorama.Fore.LIGHTYELLOW_EX)
    screen.clear()
    tx.size(screen.width, screen.height)


def startup():
    """Display startup screen"""
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
    screen.print(tx.overlay(tx.border(), logo(), tx.ln(
        tx.la("Press any key to continue."), -2)))
    screen.move(29, -4)
    wait_for_key()
    screen.clear()


def make_list(heading, options, highlight=None):
    """Display a list of items on screen"""
    h, g = 11, 3
    if len(options) > screen.height - 18:
        # TODO: trim options
        pass
    options = [' ' + x + ' ' * (71 - len(x)) for x in options]
    if highlight is not None:
        options[highlight] = cl.Fore.BLACK + cl.Back.LIGHTYELLOW_EX + \
            options[highlight] + cl.Back.RESET + cl.Fore.LIGHTYELLOW_EX
    options = zip(options, range(h + g, h + g + len(options)))
    s = tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la(heading, 4), h),
        tx.ln(tx.la('═' * 72), h + 1),
        *[tx.ln(tx.la(x[0]), x[1]) for x in list(options)]
    )
    return s


def find_key(key):
    """Parse user input"""
    if sc.using_getch:
        if key == 10:  # enter
            return 'enter'
        elif key == 27:  # special keys
            if ord(screen.read()) == 27:  # esc twice, otherwise discard '['
                return 'esc'
            key = ord(screen.read())  # get third char
            if key == 65:  # up
                return 'up'
            elif key == 66:  # down
                return 'down'
            elif key == 67:  # right
                return 'right'
            elif key == 68:  # left
                return 'left'
            elif key == 53:  # page up
                return 'pup'
            elif key == 54:  # page down
                return 'pdown'
    else:
        if key == 13:  # enter
            return 'enter'
        elif key == 27:  # esc
            return 'esc'
        elif key == 224 or key == 0:  # special keys (0 for newer terminals)
            key = ord(screen.read())  # get second char
            if key == 72:  # arrow up
                return 'up'
            elif key == 80:  # arrow down
                return 'down'
            elif key == 81:  # page down
                return 'pdown'
            elif key == 73:  # page up
                return 'pup'
    return 'dunno'


def list_handler(heading, options, *lines, go_back=False, end_line=None):
    """Asks user for a choice in a list of options"""
    lines = list(lines)
    if lines:
        lines.append('')
    choice = 0
    selected = False
    if go_back:
        options.append("Go Back")
    while not selected:
        screen.clear()
        screen.print(make_list(heading, lines + options, len(lines) + choice))
        screen.move(0, -1)
        if end_line:
            screen.print(' ' + end_line)
        key = ord(screen.read())
        key = find_key(key)
        if key == 'enter':
            selected = True
            if go_back and choice + 1 == len(options):
                return -1
            return choice
        elif key == 'esc':
            choice = -1
            selected = True
            return -1
        if key == 'up':
            choice -= 1
            if choice < 0:
                choice = len(options) - 1
        elif key == 'down':
            choice += 1
            if choice > len(options) - 1:
                choice = 0
        elif key == 'pdown':
            choice = len(options) - 1
        elif key == 'pup':
            choice = 0
    return -1


def simple_input(heading, prompt):
    """Simple single field string input"""
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


def input_form(heading, types, prompts, *lines):
    """Ask the user to fill in an input form.

    Types is a string consisting of the inputs to take.
    Three types are currently supported: string, number and password.
    
    For example, 'ssnpn' passed to types will ask for two strings, 
    one numeric value, one password and one more string in that order.

    Prompts is an array consisting of prompts for each corresponding input.
    """
    inputs = []
    lines = list(lines)
    if lines:
        lines.append('')
    for x in types:
        inputs.append((x, None))
    for i, x in enumerate(inputs):
        done = False
        ask_int = False
        ask_pass = False
        while not done:
            s = make_list(heading, lines + prompts)
            screen.clear()
            screen.print(s)
            if ask_int:
                screen.move(0, -1)
                screen.print(" Please enter a numeric value.")
            if ask_pass:
                screen.move(0, -1)
                screen.print(" Please enter a valid password.")
            screen.move(len(prompts[i]) + 6, 14 + len(lines) + i)
            if x[0] == 'p':
                import getpass
                inp = getpass.getpass(prompt='').strip()
                if ' ' in inp:
                    ask_pass = True
                    continue
            else:
                inp = input().strip()
            if x[0] == 'n':
                try:
                    inputs[i] = (x[0], float(inp))
                except ValueError:
                    if not inp:
                        inputs[i] = (x[0], 0)
                    else:
                        ask_int = True
                        continue
            else:
                inputs[i] = (x[0], inp)
            prompts[i] += ' ' + inp
            done = True
    return [x[1] for x in inputs]


def display_info(heading, *lines, end_line='Press any key to continue.'):
    """Display a set of lines on screen"""
    screen.clear()
    screen.print(make_list(heading, lines))
    screen.move(0, -1)
    if end_line:
        screen.print(' ' + end_line)
    wait_for_key()


def finish():
    """Display the exit screen"""
    screen.clear()
    random.seed(time.time())
    backs = random.sample([cl.Back.MAGENTA,
                           cl.Back.GREEN,
                           cl.Back.RED,
                           cl.Back.YELLOW,
                           cl.Back.LIGHTRED_EX,
                           cl.Back.LIGHTBLACK_EX,
                           cl.Back.LIGHTMAGENTA_EX,
                           cl.Back.MAGENTA], 8)
    screen.print(cl.Fore.BLACK + random.choice(backs) + tx.overlay(
        tx.border(),
        logo(),
        tx.ln(tx.la("Have a nice day!"), -2),
        tx.ln(tx.la("Thanks for using bank9000™."), -3)
    ))
    time.sleep(2)
    screen.print(cl.Fore.RESET + cl.Back.RESET)
    screen.clear()
    screen.print("bank9000™\n")
