def transfer(ac, frm, to, amt):
    ac.mod_balance(frm, -amt)
    ac.mod_balance(to, amt)


def handle(acc, ac, ci):
    account_not_found = False
    insufficient_funds = False
    thief = False
    ch = 0
    while True:
        if account_not_found:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "Account number " + inp[0] + " not found.")
        elif insufficient_funds:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "You do not have sufficient funds to complete this transaction.")
        elif thief:
            ch = ci.list_handler('Account Login', ['Try Again', 'Go Back'],
                                 "Please input a valid amount to transfer")
        if ch:
            return None
        inp = ci.input_form("Transfer Funds", 'sn', ['Account Number/Username:', 'Amount to Transfer:'])
        if inp[1] < 0:
            thief = False
            continue
        if inp[1] < ac.get_balance_raw(acc):
            insufficient_funds = True
        if inp[1] == 0:
            return None
        try:
            acc_to = ac.find(inp[0].strip())
        except ac.AccountNotFoundError:
            account_not_found = True
            continue
        transfer(ac, acc, acc_to, inp[1])
        return None
