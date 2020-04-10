import requests

rates = {
    "CAD": 0.0185041171,
    "HKD": 0.1097273051,
    "ISK": 1.7573955474,
    "PHP": 0.7221332723,
    "DKK": 0.0949209617,
    "HUF": 4.2235945918,
    "CZK": 0.3280979974,
    "GBP": 0.0110625699,
    "RON": 0.0604071363,
    "SEK": 0.1375228728,
    "IDR": 198.1221408966,
    "INR": 1.0,
    "BRL": 0.0577754905,
    "RUB": 0.9015146894,
    "HRK": 0.0944812951,
    "JPY": 1.5150706516,
    "THB": 0.4248500559,
    "CHF": 0.0139486124,
    "EUR": 0.0127071262,
    "MYR": 0.0586116194,
    "BGN": 0.0248525973,
    "TRY": 0.0821871506,
    "CNY": 0.0990431534,
    "NOK": 0.1279010369,
    "NZD": 0.0223022771,
    "ZAR": 0.2078758768,
    "USD": 0.0139867338,
    "MXN": 0.268942513,
    "SGD": 0.0191725119,
    "AUD": 0.0207037206,
    "ILS": 0.0492833181,
    "KRW": 16.5892802684,
    "PLN": 0.0545847311
}


try:
    data = requests.get("https://api.exchangeratesapi.io/latest?base=INR")
    if data.status_code == 200:
        rates = data.json()['rates']
except Exception as e:  # should work on this
    pass


def convert(frm, to, value):
    """Convert a currency"""
    amount = value * rates[to] / rates[frm]
    return amount


def currencies():
    """Returns supported currencies"""
    return rates.keys()


if __name__ == '__main__':
    value = input("Please enter amount :")
    value = int(value)
    frm = input("Please enter the currency you have : ")
    to = input("please enter the foreign currency you want : ")
    convert(frm, to, value)
