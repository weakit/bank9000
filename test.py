#!/usr/bin/env python3
import screen as sc
import time
import texty as t
import interface

if __name__ == "__main__":
    """Screen Test"""
    t.size(sc.width, sc.height)
    print("Screen clear test.\nWill attempt to clear screen in 3s.")
    time.sleep(3)
    sc.clear()
    print(sc.colorama.Fore.LIGHTGREEN_EX + "Screen cleared." + sc.colorama.Fore.RESET)
    time.sleep(1)
    sc.clear()
    print("Border detection tests.\nWill attempt to find console size and print borders.")
    print("width: ", sc.width, "height: ", sc.height)
    time.sleep(2)
    sc.clear()
    print(t.overlay(t.border(), t.ca('\n' * 9 + "logo test."),
                    t.ca(interface.logo())), end='')
    sc.move()
    time.sleep(3)
    sc.clear()
    print(t.overlay(t.border(), t.border(20, 10), t.border(10, 20)), end='')
    sc.move()
    time.sleep(1)
    print("Basic Tests Complete.")
    sc.clear()  # clear on exit
