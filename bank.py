import interface as ci
import accounts as ac
import time


def new_account():
    done = False
    ask = False
    while not done:
        if not ask:
            info = ci.input_form('Account Details', 'sss', ['Name:', 'Username:', 'Password:'])
        else:
            info = ci.input_form('Account Details', 'sss', ['Name:', 'Username:', 'Password:'],
                                 'That username is already taken.')
        if ac.available(info[1]):
            done = True
        else:
            ask = True

    ac.make_account_low(*info)
    acc_no = ac.find(info[1])
    acc = ac.get_account(acc_no)
    ci.display_info("Account Details",
                    "Your account has been created successfully.", '',
                    "Account No: " + ac.pretty_no(acc_no),
                    "Account Name: " + acc['name'],
                    "Username: " + acc['user'], '',
                    "Press any key to continue.")
    ci.wait_for_enter()


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
