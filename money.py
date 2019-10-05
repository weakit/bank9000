def uncredited(acc, ac, ci):
    make_withdrawal, make_deposit, insufficient_funds, succeeded = False, False, False, False
    end = ''
    while True:
        op = ['Make a Withdrawal', 'Make a Deposit', 'Go Back']
        if succeeded:
            end = 'Transaction completed successfully.'
        elif make_withdrawal:
            end = 'Use the Withdrawal menu option to withdraw funds.'
        elif make_deposit:
            end = 'Use the Deposit menu option to deposit funds.'
        elif insufficient_funds:
            end = 'Your account does not have sufficient funds.'
        choice = ci.list_handler('Withdrawals and Deposits', op,
                                 "Current Balance: Rs. " + str(ac.get_balance(acc)), end_line=end)
        make_withdrawal, make_deposit, insufficient_funds, succeeded = False, False, False, False
        opdo = {0: withdraw, 1: deposit, 2: lambda *a: True, -1: lambda *a: True}
        c = opdo[choice](acc, ac, ci)
        if c is True:
            return None
        elif c is None:
            pass
        elif c == -420:
            succeeded = True
        elif c == -3214:
            make_deposit = True
        elif c == -5489:
            insufficient_funds = True
        elif c == -8734:
            make_withdrawal = True


def withdraw(acc, ac, ci):
    cur_bal = ac.get_balance(acc)
    amt = ci.input_form("Withdraw Funds", 'n', ["Amount to Withdraw:"], "Current Balance: Rs. " + str(cur_bal))[0]
    if not amt:
        return None
    if amt < 0:
        return -3214
    if amt > cur_bal:
        return -5489
    cur_bal -= amt
    ac.set_balance(acc, cur_bal)
    return -420


def deposit(acc, ac, ci):
    cur_bal = ac.get_balance(acc)
    amt = ci.input_form("Deposit Funds", 'n', ["Amount to Deposit:"], "Current Balance: Rs. " + str(cur_bal))[0]
    if not amt:
        return None
    if amt < 0:
        return -8734
    cur_bal += amt
    ac.set_balance(acc, cur_bal)
    return -420
