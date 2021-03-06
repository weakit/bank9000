import json
from datetime import datetime
import base64
import zlib
import hashlib
import string
import random

default = {
    'name': 'Account Name',
    'age': 0,
    'user': 'user',
    'pass': '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    'balance': 0,
    'loan': [],
    'history': []
}

users = {}
accounts = {}


class AccountNotFoundError(Exception):
    def __init__(self, account):
        self.account = account

    def __str__(self):
        return "account '" + str(self.account) + "' not found"


def account_number():
    """Generates a random account number"""
    s = ""
    for x in range(4):
        s += random.choice(string.ascii_uppercase)
    for x in range(7):
        s += random.choice(string.digits)
    return s


def pretty_no(n, reverse=False):
    """Formats an account number"""
    if reverse:
        return ''.join(n.split(' '))
    s = ''
    while len(n) > 4:
        s += n[:4] + ' '
        n = n[4:]
    s += n
    return s.strip()


def read():
    """Read accounts from disk"""
    global accounts, users
    try:
        f = open("accounts.dat", "rb")
    except FileNotFoundError:
        return None
    rd = f.read()
    users, accounts = json.loads(base64.b64decode(zlib.decompress(rd[65:])).decode())
    f.close()


def write():
    """Write accounts to disk"""
    f = open("accounts.dat", "wb")
    f.write(("bank9000™ accounts data\nwritten UTC " + str(datetime.utcnow()) + '\n').encode('utf-8'))
    s = base64.b64encode(json.dumps((users, accounts)).encode())
    f.write(zlib.compress(s) + b'\n')
    f.close()


def available(n):
    """Check if username is available"""
    read()
    return n not in users.keys()


def make_account_low(name, user, password):
    """Make an account"""
    ac = default
    ac['name'] = name
    ac['user'] = user
    ac['pass'] = hashlib.sha256(password.encode()).hexdigest()
    ac_no = account_number()
    read()
    while ac_no in accounts.keys():
        ac_no = account_number()
    accounts[ac_no] = ac
    users[user] = ac_no
    write()
    return ac_no, ac


def delete_account(n):
    """Delete account"""
    read()
    if n in users.keys():
        ac_no = users.pop(n)
        del(accounts[ac_no])
    elif n in accounts.keys():
        user = accounts[n]['user']
        del(accounts[n])
        del(users[user])
    write()


def find(n):
    """Search for account number/username"""
    read()
    if n.lower() in users.keys():
        n = users[n]
    if n not in accounts:
        raise AccountNotFoundError(n)
    return n


def check_pass(n, password):
    """Check if password matches"""
    n = find(n)
    if accounts[n]['pass'] == hashlib.sha256(password.encode()).hexdigest():
        return True
    return False


def get_account(n):
    """Get an account"""
    n = find(n)
    return accounts[n]


def get_accounts():
    """Returns all accounts"""
    return list(accounts.keys())


def get_name(n):
    """Get name of account"""
    n = find(n)
    return accounts[n]['name']


def set_name(n, new_name):
    """Set name of account"""
    global accounts
    n = find(n)
    accounts[n]['name'] = new_name
    write()


def get_user(n):
    """Get username of account"""
    n = find(n)
    return accounts[n]['user']


def set_user(n, new_user):
    """Set username of account"""
    global accounts
    n = find(n)
    accounts[n]['user'] = new_user
    write()


def get_balance(n):
    """Get balance of account"""
    n = find(n)
    b = accounts[n]['balance']
    if float(b).is_integer():
        return int(b)
    return round(b, 2)


def get_balance_raw(n):
    """Get unrounded balance of account"""
    n = find(n)
    return accounts[n]['balance']


def set_balance(n, new_balance):
    """Set balance of account"""
    global accounts
    n = find(n)
    accounts[n]['balance'] = new_balance
    write()


def mod_balance(n, mod_balance):
    """Add to balance of account"""
    global accounts
    n = find(n)
    accounts[n]['balance'] += mod_balance
    write()


def get_age(n):
    """Get age of account"""
    n = find(n)
    return accounts[n]['age']


def set_age(n, new_age):
    """Set age of account"""
    global accounts
    n = find(n)
    accounts[n]['age'] = new_age
    write()
