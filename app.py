from calendar import c
from helpers import apology, login_required, usd, eur, gbp, uah, rub, format, verify_card, left_to_spend
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from asyncio.windows_utils import PipeHandle
from datetime import datetime
import os
import re

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["format"] = format
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["eur"] = eur
app.jinja_env.filters["gbp"] = gbp
app.jinja_env.filters["uah"] = uah
app.jinja_env.filters["rub"] = rub

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///skybank.db")

currencies = {'usd': '$', 'eur': '€', 'gbp': '£', 'uah': '₴', 'rub': '₽'}


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Main page"""
    # Client dict
    client = db.execute(
        "SELECT * FROM accounts WHERE id = ?", session["user_id"])[0]

    # Transactions
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER by id DESC", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        limit = request.form.get("limit")

        # Ensure limit was submitted
        if not limit:
            return apology("must provide limit", 400)

        # Ensure limit is valid
        try:
            limit = int(limit)
        except (KeyError, TypeError, ValueError):
            return apology("invalid limit value", 400)

        if limit < 0:
            return apology("invalid limit value", 400)
        if limit < (left_to_spend(transactions, client["m_limit"]) - client["m_limit"]):
            return apology("Such sum was already spent", 400)

        # Update balance
        db.execute("UPDATE accounts SET m_limit=? WHERE id=?",
                   limit, session["user_id"])

        return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Split card number
        card = str(client["card_num"])
        client["card"] = [card[0:4], card[4:8], card[8:12], card[12:16]]

        # Format expiration month
        if len(client["expiration"]) == 4:
            client["expiration"] = f"0{client['expiration']}"

        # Get currency sign
        client["sign"] = currencies[f"{client['currency']}"]

        for row in transactions:
            if row["op_type"] == "in":
                row["sign"] = '+'
            else:
                row["sign"] = '-'

        # Left to spend this month
        left = left_to_spend(transactions, client["m_limit"])

        # Render page
        return render_template("index.html", client=client, transactions=transactions, left=left)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Change clients`s pin"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form data
        pin = request.form.get("pin")
        new_pin = request.form.get("new_pin")

        # Ensure password was submitted
        if not pin:
            return apology("must provide pin", 400)

        # Ensure new password was submitted
        if not new_pin:
            return apology("must provide new pin", 400)

        # Ensure pins match
        if new_pin != request.form.get("confirmation"):
            return apology("pins do not match", 400)

        # Ensure pin is valid
        rows = db.execute(
            "SELECT * FROM accounts WHERE id = ?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], pin):
            return apology("invalid password", 403)

        # Update database
        db.execute("UPDATE accounts SET hash=? WHERE id=?",
                   generate_password_hash(new_pin), session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure login was submitted
        if not request.form.get("login"):
            return apology("must provide login", 403)

        # Ensure pin was submitted
        if not request.form.get("pin"):
            return apology("must provide PIN", 403)

        # Query database for login
        rows = db.execute(
            "SELECT * FROM accounts WHERE login = ?", request.form.get("login"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("pin")):
            return apology("invalid login and/or PIN", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register client"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form data
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        pay_sys = request.form.get("pay-sys")
        currency = request.form.get("currency")
        deposit = request.form.get("deposit")
        login = request.form.get("login")
        pin = request.form.get("pin")
        confirmation = request.form.get("confirmation")
        agree = request.form.get("agree")

        # Ensure everything is submitted
        if not name:
            return apology("must provide name", 400)
        if not lastname:
            return apology("must provide last name", 400)
        if not pay_sys:
            return apology("must provide payment system", 400)
        if not currency:
            return apology("must provide currency", 400)
        if not deposit:
            return apology("must provide deposit", 400)
        if not login:
            return apology("must provide login", 400)
        if not pin:
            return apology("must provide pin", 400)
        if not confirmation:
            return apology("must provide confirmation", 400)
        if not agree:
            return apology("must agree with terms and conditions", 400)

        # Ensure PINs match
        if pin != confirmation:
            return apology("passwords do not match", 400)

        # Ensure PIN is 4-digit value
        if not re.match('^\d\d\d\d$', pin):
            return apology("pin must be 4-digit value", 400)

        # Ensure login is unique value
        rows = db.execute("SELECT * FROM accounts WHERE login = ?", login)
        if len(rows) != 0:
            return apology("login is already taken", 400)

        # Ensure currency is valid
        if currency not in currencies.keys():
            return apology("invalid currency", 400)

        # Validate payment system
        if pay_sys != "visa" and pay_sys != "mastercard":
            return apology(f"{pay_sys}", 400)

        # Validate deposit
        try:
            deposit = int(deposit)
        except (KeyError, TypeError, ValueError):
            return apology("invalid deposit sum", 400)
        if deposit < 1000:
            return apology('deposit sum is less than 1000', 400)

        # Get card number
        card_number = db.execute(
            "SELECT number FROM cards WHERE user_id=1 and pay_sys=?", pay_sys)[0]["number"]

        # Define expiration date
        month = datetime.now().month
        year = int(str(datetime.now().year)[2:4]) + 5
        expiration = f"{month}/{year}"

        # Insert user into database
        db.execute(
            "INSERT INTO accounts (name, lastname, login, hash, currency, pay_sys, card_num, expiration, cash) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            name, lastname, login, generate_password_hash(pin), currency, pay_sys, card_number, expiration, deposit)

        # Assign card number to user
        user = db.execute(
            "SELECT id, card_num FROM accounts WHERE login=?", login)[0]
        db.execute("UPDATE cards SET user_id=? WHERE number=?",
                   user["id"], user["card_num"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/top_up", methods=["GET", "POST"])
@login_required
def top_up():
    # Client`s info
    client = db.execute(
        "SELECT * FROM accounts WHERE id=?", session["user_id"])[0]
    cash = client["cash"]
    sign = currencies[f"{client['currency']}"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        sources = ['atm', 'card', 'credit', 'bless', 'birthday']

        # Get form data
        source = request.form.get("source")
        sum = request.form.get("sum")

        # Ensure source was submitted
        if not source:
            return apology("must provide source", 400)

        # Ensure source is valid
        if source not in sources:
            return apology("invalid source", 400)

        # Ensure sum was submitted
        if not sum:
            return apology("must provide sum", 400)

        # Ensure sum is valid
        if int(sum) < 0:
            return apology("invalid sum", 400)

        # Update balance
        db.execute("UPDATE accounts SET cash=? WHERE id=?",
                   (cash + int(sum)), session["user_id"])

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, sum, address, op_type, time) VALUES(?, ?, ?, ?, ?)",
            session["user_id"], sum, source, 'in', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("top-up.html", cash=cash, sign=sign)


@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    # Client`s info
    client = db.execute(
        "SELECT * FROM accounts WHERE id=?", session["user_id"])[0]
    cash = client["cash"]
    sign = currencies[f"{client['currency']}"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER by id DESC", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form data
        address = request.form.get("address")
        sum = request.form.get("sum")

        # Ensure address was submitted
        if not address:
            return apology("must provide address", 400)

        # Ensure address is valid
        try:
            address = int(address)
        except (KeyError, TypeError, ValueError):
            return apology("invalid address value", 400)

        if not verify_card(address):
            return apology("invalid card number", 400)

        # Ensure sum was submitted
        if not sum:
            return apology("must provide sum", 400)

        # Ensure sum is valid
        if int(sum) < 0:
            return apology("invalid sum", 400)

        # Ensure sufficient funds
        if int(sum) > cash:
            return apology("Insufficient funds", 400)

        # Ensure within limit
        if left_to_spend(transactions, client["m_limit"]) < int(sum):
            return apology("Sum of payment is beyond monthly payments limit", 400)

        # Update balance
        db.execute("UPDATE accounts SET cash=? WHERE id=?",
                   (cash - int(sum)), session["user_id"])

        # Record transaction
        address = f"{address}/{verify_card(address)}"
        db.execute(
            "INSERT INTO transactions (user_id, sum, address, op_type, time) VALUES(?, ?, ?, ?, ?)",
            session["user_id"], sum, address, 'out', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("transfer.html", cash=cash, sign=sign)


@app.route("/payments", methods=["GET", "POST"])
@login_required
def payments():
    # Client`s info
    client = db.execute(
        "SELECT * FROM accounts WHERE id=?", session["user_id"])[0]
    cash = client["cash"]
    sign = currencies[f"{client['currency']}"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER by id DESC", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form data
        address = request.form.get("address")
        sum = request.form.get("sum")

        # Ensure address was submitted
        if not address:
            return apology("must provide phone number", 400)

        # Ensure address is valid
        if len(address) != 10:
            return apology("invalid phone number", 400)

        try:
            check = int(address)
        except (KeyError, TypeError, ValueError):
            return apology("invalid address value", 400)

        # Ensure sum was submitted
        if not sum:
            return apology("must provide sum", 400)

        # Ensure sum is valid
        if int(sum) < 0:
            return apology("invalid sum", 400)

        # Ensure sufficient funds
        if int(sum) > cash:
            return apology("Insufficient funds", 400)

        # Ensure within limit
        if left_to_spend(transactions, client["m_limit"]) < int(sum):
            return apology("Sum of payment is beyond monthly payments limit", 400)

        # Update balance
        db.execute("UPDATE accounts SET cash=? WHERE id=?",
                   (cash - int(sum)), session["user_id"])

        # Record transaction
        address = f"{address}/mobile credit"
        db.execute(
            "INSERT INTO transactions (user_id, sum, address, op_type, time) VALUES(?, ?, ?, ?, ?)",
            session["user_id"], sum, address, 'out', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("payments.html", cash=cash, sign=sign)


if __name__ == '__main__':
    app.run(debug=True)
