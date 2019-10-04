import interface as ci
import accounts as ac


def new_account():
    pass


def login():
    pass


def finish():
    ci.finish()
    exit()


if __name__ == '__main__':
    ci.init()
    ci.startup()
    opdc = {
        0: new_account,
        1: login,
        2: finish
    }
    while True:
        op = ci.list_handler('', ['Open a new bank9000™ Account', 'Log into your existing bank9000™ Account', 'Exit'])
        opdc[op]()
