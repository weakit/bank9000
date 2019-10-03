import screen
import texty as tx
import time

logo = """

    ██████╗  █████╗ ███╗   ██╗██╗  ██╗  █████╗  ██████╗  ██████╗  ██████╗ TM
    ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝ ██╔══██╗██╔═████╗██╔═████╗██╔═████╗
    ██████╔╝███████║██╔██╗ ██║█████╔╝  ╚██████║██║██╔██║██║██╔██║██║██╔██║
    ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗   ╚═══██║████╔╝██║████╔╝██║████╔╝██║
    ██████╔╝██║  ██║██║ ╚████║██║  ██╗  █████╔╝╚██████╔╝╚██████╔╝╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝  ╚════╝  ╚═════╝  ╚═════╝  ╚═════╝ 
                                                   a bank you can trust
    
    
"""

if __name__ == '__main__':
    screen.print(screen.colorama.Fore.LIGHTYELLOW_EX)
    screen.clear()
    tx.size(screen.width, screen.height)
    startup_screen = tx.overlay(
        tx.border(),
        logo,
        tx.ln(tx.la("Starting BMS"), -2)
    )
    screen.print(startup_screen)
    screen.move(15, -4)
    time.sleep(1)
    screen.clear()
    screen.print(tx.overlay(tx.border(), logo, tx.ln(tx.la("Press enter to continue."), -2)))
    screen.move(27, -4)
    input()
    screen.clear()
