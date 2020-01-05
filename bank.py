#!/usr/bin/env python3
import interface as ci
import accounts as ac
import money
import currencies
import timesim
import transfers
import demands


def handle_account(acc):
    while True:
        ch = ci.list_handler('Account ' + ac.pretty_no(acc),
                             ["Withdrawals and Deposits", "Money Transfers",
                              "Demand Drafts", "Currency Conversions", "Logout"],
                             "Account Holder's Name: " + ac.get_name(acc),
                             "Username: " + ac.get_user(acc),
                             'Current Account Balance: Rs. ' + str(ac.get_balance(acc)))
        chop = {0: money.uncredited, 1: transfers.handle, 2: demands.handle,
                3: handle_currencies, 4: lambda *a: True, -1: lambda *a: True}
        c = chop[ch](acc, ac, ci)
        if c:
            return None


def handle_currencies(*args):
    supported = currencies.currencies()
    s = ["Supported Currencies:", '\n']
    st = ''
    for i, x in enumerate(supported):
        st += x + ' '
        if not (i + 1) % 10:
            s.append(st)
            st = ''
    s.append('\n')
    unsupported = weird_value = nothing = False
    while True:
        if nothing:
            if ci.list_handler('Account Login', ['Try Again', 'Go Back'], 'Please enter valid input.'):
                return None
        if weird_value:
            s[-1] = "Invalid value"
        if unsupported:
            s[-1] = "Unsupported Currency."
        unsupported = weird_value = nothing = False
        inp, to = ci.input_form('Currency Conversions',
                                'ss', ["Convert:", "To:"], *s)
        if not inp or not to:
            nothing = True
            continue
        inp = inp.replace(' ', '').upper()
        to = to.replace(' ', '').upper()
        frm = inp[-3:]
        if frm not in supported or to not in supported:
            unsupported = True
            continue
        try:
            value = float(inp[:-3])
        except ValueError:
            weird_value = True
            continue
        break
    converted_value = round(currencies.convert(frm, to, value), 4)
    ci.display_info("Currency Conversions", str(value) + ' ' +
                    frm + ' = ' + str(converted_value) + ' ' + to)


def new_account():
    done = ask = no_pass = no_user = False
    ch = 0
    while not done:
        if ask:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 'That username is already taken.')
        elif no_pass:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 'You have not entered a password.')
        elif no_user:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 'You have not entered a username.')
        if ch:
            return None
        done = ask = no_pass = no_user = False
        info = ci.input_form('Account Details', 'ssp', [
                             'Name:', 'Username:', 'Password:'])
        if not info[0]:
            info[0] = "Anonymous"
        if not info[2]:
            no_pass = True
            continue
        if not info[1]:
            no_user = True
            continue
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
    ci.wait_for_key()


def login():
    done = non_existent = wrong_pass = False
    ch = 0
    while not done:
        if non_existent:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "The account you are trying to login to does not exist.")
        elif wrong_pass:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "The password you have entered is incorrect.")
        if ch:
            return None
        done = non_existent = wrong_pass = False
        cred = ci.input_form("Account Login", 'sp', [
                             'Account Number/Username:', 'Password:'])
        try:
            acc = ac.find(cred[0])
        except ac.AccountNotFoundError:
            non_existent = True
            continue
        if not ac.check_pass(acc, cred[1]):
            wrong_pass = True
            continue
        handle_account(acc)
        return None


def finish():
    ci.finish()
    exit()


def simulate_time():
    timesim.handle(ac, ci, 9)


if __name__ == '__main__':
    ci.init()
    ci.startup()
    opdc = {
        0: new_account,
        1: login,
        2: simulate_time,
        3: handle_currencies,
        4: finish
    }
    while True:
        op = ci.list_handler('', ['Open a new bank9000™ Account',
                                  'Login with your existing bank9000™ Account',
                                  'Simulate Passage of Time',
                                  'Currency Conversions',
                                  'Exit'])
        opdc[op]()
