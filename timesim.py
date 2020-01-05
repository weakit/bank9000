def handle(ac, ci, rate):
    """Handle Time Simulations"""
    x = ci.input_form("Time Simulator", 'n', ["Days to Simulate:"],
                      "bank9000 offers an unbelievable interest rate of " + str(rate) + "% pa")
    simulate(ac, x[0], rate)
    ci.display_info("Time Simulator", str(x[0]) + " days have been simulated.")


def simulate(ac, days, rate):
    """Simulates passage of time"""
    ac.read()
    for account in ac.get_accounts():
        balance = ac.get_balance_raw(account)
        age = ac.get_age(account)
        t = age % 30 + days
        balance = balance + (balance * (t/365) * rate/100)
        ac.set_balance(account, balance)
        ac.set_age(account, days+age)


def db_reset(ac):
    """[DO NOT USE] Reset account values. For debugging only."""
    ac.read()
    for x in ac.get_accounts():
        ac.set_balance(x, 100)
        ac.set_age(x, 0)
