import os
import requests
import urllib.parse

from datetime import datetime
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https:#github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https:#flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Ensure card is valid."""
    return


def format(value):
    """Format value."""
    return f"{value:,.2f}"


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def eur(value):
    """Format value as EUR."""
    return f"€{value:,.2f}"


def gbp(value):
    """Format value as GBP."""
    return f"£{value:,.2f}"


def uah(value):
    """Format value as UAH."""
    return f"₴{value:,.2f}"


def rub(value):
    """Format value as EUR."""
    return f"₽{value:,.2f}"


def verify_card(input):
    input = str(input)
    sumMult = 0
    sumOrd = 0

    # Iterate through the card
    for i in reversed(range(0, len(input))):
        # Current digit
        n = int(input[i])

        # Check if digit is other
        if i % 2 == 0:
            # Check if digit is greater then 4, as multiplied by 2 will be a two digit
            if n > 4:
                # Identify first and last digits and sum them with other multiplied digits
                last = (n * 2) % 10
                first = (n * 2 - last) / 10
                sumMult += last + first
            else:
                # Digit is 4 or less so just add it
                sumMult += n * 2
        else:
            # these ones are not multiplied, just sum them together
            sumOrd += n

    # Last digit of total sum is 0
    if ((sumMult + sumOrd) % 10 == 0):
        first_two = int(input[0:2])
        first_d = int(input[0:1])

        if (first_two == 34 or first_two == 37) and len(input) == 15:
            return 'amex'
        if (first_two == 51 or first_two == 52 or first_two == 53 or first_two == 54 or first_two == 55) and len(input) == 16:
            return 'mastercard'
        if first_d == 4 and (len(input) == 15 or len(input) == 16):
            return 'visa'

    # Else
    return False


def left_to_spend(transactions, limit):
    month = str(datetime.now().month)
    year = datetime.now().year
    if len(month) == 1:
        month = "0" + month
    l = list(filter(lambda x: x["time"][3:10]
                    == f"{month}/{year}" and x["op_type"] == 'out', transactions))
    spent = 0

    for tr in l:
        spent += int(tr["sum"])

    return limit - spent
