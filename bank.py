import interface as ci
import accounts as ac
import money
import currencies
import timesim


def handle_account(acc):
    while True:
        ch = ci.list_handler('Account ' + ac.pretty_no(acc),
                             ["Withdrawals and Deposits", "Money Transfers",
                              "Demand Drafts", "Currency Conversions", "Logout"],
                             "Account Holder's Name: " + ac.get_name(acc),
                             "Username: " + ac.get_user(acc),
                             'Current Account Balance: Rs. ' + str(ac.get_balance(acc)))
        chop = {0: money.uncredited, 1: lambda *a: None, 2: lambda *a: None,
                3: handle_currencies, 4: lambda *a: True, -1: lambda *a: True}
        c = chop[ch](acc, ac, ci)
        if c:
            return None


def handle_currencies(acc, ac, ci):
    supported = currencies.currencies()
    pass


def new_account():
    done = False
    ask = False
    no_pass = False
    no_user = False
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
        info = ci.input_form('Account Details', 'ssp', ['Name:', 'Username:', 'Password:'])
        if not info[0]:
            info[0] = "Anonymous"
        if not info[2]:
            no_pass = True
            no_user = False
            ask = False
            continue
        if not info[1]:
            no_user = True
            no_pass = False
            ask = False
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
    ci.wait_for_enter()


def login():
    done = False
    non_existent = False
    wrong_pass = False
    ch = 0
    while not done:
        if non_existent:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "The account you are trying to login to does not exist.")
        elif wrong_pass:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "The password you have entered is incorrect.")
        if non_existent or wrong_pass:
            if ch:
                return None
        cred = ci.input_form("Account Login", 'sp', ['Account Number/Username:', 'Password:'])
        try:
            acc = ac.find(cred[0])
        except ac.AccountNotFoundError:
            non_existent = True
            wrong_pass = False
            continue
        if not ac.check_pass(acc, cred[1]):
            non_existent = False
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
        3: finish
    }
    while True:
        op = ci.list_handler('', ['Open a new bank9000™ Account',
                                  'Login with your existing bank9000™ Account', 'Simulate Time', 'Exit'])
        opdc[op]()
