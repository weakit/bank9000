import json
import base64
from datetime import datetime
import zlib
import string
import random

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
    f = open('demands.dat', 'wb+')
    f.write(("bank9000™ demands data\nwritten UTC " + str(datetime.utcnow()) + '\n').encode('utf-8'))
    p = zlib.compress(base64.b64encode(json.dumps(dds).encode()))
    f.write(p + b'\n')
    f.close()


def del_dd(dd_num):
    read()
    if dd_num in dds.keys():
        del(dds[dd_num])
    write()


def make_dd(acc, amt):
    read()
    dd_num = dd_no()
    while dd_num not in dds.keys():
        dd_num = dd_no()
    dd = {
        'ac_no': acc,
        'amount': amt
    }
    dds[dd_num] = dd
    write()


if __name__ == '__main__':
    write()

