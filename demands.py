import json
import base64
from datetime import datetime
import zlib
import string
import random

ac = None
ci = None


default = {
    "ac_no": "ABCD1234567",
    "amount": 0
}

dds = {"ABC123456": default}


def dd_no():
    s = ""
    for x in range(3):
        s += random.choice(string.ascii_uppercase)
    for x in range(6):
        s += random.choice(string.digits)
    return s


def read():
    global dds
    try:
        f = open('demands.dat', 'rb')
    except FileNotFoundError:
        return None
    a = f.read()
    dds = json.loads(base64.b64decode(zlib.decompress(a[64:])))


def write():
    f = open('demands.dat', 'wb')
    f.write(("bank9000™ demands data\nwritten UTC " + str(datetime.utcnow()) + '\n').encode('utf-8'))
    p = zlib.compress(base64.b64encode(json.dumps(dds).encode()))
    f.write(p + b'\n')
    f.close()


def del_dd(dd_num):
    read()
    if dd_num in dds.keys():
        del(dds[dd_num])
    write()


def write_dd(dd_num, dd):
    global dds
    read()
    dds[dd_num] = dd
    write()


def gen_dd(acc, amt):
    read()
    dd_num = dd_no()
    while dd_num in dds.keys():
        dd_num = dd_no()
    dd = {
        'ac_no': acc,
        'amount': amt
    }
    return dd_num, dd


def issue(acc, amt):
    if amt <= 0:
        return -69
    if ac.get_balance_raw(acc) < amt:
        return -420
    ac.mod_balance(acc, -amt)
    dd_num, dd = gen_dd(acc, amt)
    write_dd(dd_num, dd)
    return dd_num


def deposit(acc, dd_num):
    if dd_num not in dds.keys():
        return -69
    original_acc, amt = dds[dd_num]['ac_no'], dds[dd_num]['amount']
    ac.mod_balance(acc, amt)
    del_dd(dd_num)
    return original_acc, amt


def handle(acc, acx, cix):
    global ac, ci
    ac, ci = acx, cix
    op = ['Create a Demand Draft', 'Claim a Demand Draft', 'Go Back']
    ch = ci.list_handler("Demand Drafts", op)
    if ch == 0:
        handle_creation(acc)
    if ch == 1:
        handle_claim(acc)


def handle_creation(acc):
    insufficient_funds = invalid = False
    ch = 0
    while True:
        if insufficient_funds:
            ch = ci.list_handler('Demand Drafts', ['Try Again', 'Go Back'],
                                 'You do not have sufficient funds.')
        if invalid:
            ch = ci.list_handler('Demand Drafts', ['Try Again', 'Go Back'],
                                 'Please input a valid amount.')
        if ch:
            return None
        invalid = insufficient_funds = False
        x = ci.input_form('Demand Draft Creation', 'n', ['Enter Amount:'])[0]
        a = issue(acc, x)
        if a == -420:
            insufficient_funds = True
            continue
        if a == -69:
            invalid = True
            continue
        ci.display_info('Demand Drafts', 'Demand Draft Created Successfully', 'Demand Draft No. ' + a)
        return None


def handle_claim(acc):
    invalid = False
    while True:
        if invalid:
            if ci.list_handler('Demand Drafts', ['Try Again', 'Go Back'], 'Demand Draft Number does not exist.'):
                return None
        s = ci.input_form("Claim Demand Draft", 's', ['Enter Demand Draft No:'])[0]
        d = deposit(acc, s.replace(' ', '').upper())
        if d == -69:
            invalid = True
            continue
        ci.display_info('Demand Drafts', 'Demand Draft Claimed Successfully')
        return None


if __name__ == '__main__':
    read()
    write()
    print(dds)
