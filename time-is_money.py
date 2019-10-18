import time
import threading

ac = None

accounts = {'XYVN5553961': {'name': 'rosh', 'age': 0, 'user': 'rosh', 'pass': 'cdd661a2435332c0a9c6601b8d174a90ac2e30a17bfdcf4882851a9d81c3f3af', 'balance': 69.0, 'loan': [], 'history': []}, 'HSQF8489172': {'name': 'Anonymous', 'age': 0, 'user': 'money', 'pass': '8d2ac8b58ead9744d77286de9b0bcb7a894f238c3149fc9f3b1e3caff36330fe', 'balance': 0, 'loan': [], 'history': []}}

rate = 0.01


def init(x):
    global ac
    ac = x


def simulate_time(n):
    global balance
    balance += balance * rate * n


def func(n):
    while True:
        simulate_time(1)
        time.sleep(n)


if __name__ == '__main__':
    a = threading.Thread(target=func)
    b = threading.Thread(target=func)
    a.start()
    time.sleep(0.5)
    b.start()
