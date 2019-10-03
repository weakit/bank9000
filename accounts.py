import json
from datetime import datetime
import base64

"""
Account Structure
 account holder name
 account number
 account age (in days)
 username
 hashed password
 account balance
 loan list (wip)
 transaction history (list of strings)
"""

default = {
    'name': 'Account Name',
    'no': 'Account Number',
    'age': 0,
    'username': 'user',
    'pass': '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    'balance': 0,
    'loan': [],
    'history': []
}

accounts = []


def read():
    global accounts
    f = open("accounts.dat", "r+")
    accounts = [json.loads(base64.b64decode(x)) for x in f.readlines()[2:]]
    f.close()


def write():
    f = open("accounts.dat", "w+")
    f.write("bank9000™ accounts data\nwritten UTC " + str(datetime.utcnow()) + '\n')
    for x in accounts:
        f.write(base64.b64encode(json.dumps(x).encode()).decode() + '\n')
    f.close()


if __name__ == '__main__':
    read()
    print(accounts)
    write()
