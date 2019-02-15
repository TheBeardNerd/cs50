import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # create user portfolio in database
    db.execute("CREATE TABLE IF NOT EXISTS portfolio (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, symbol TEXT, name TEXT, shares INTEGER, price, purchase_date, value, FOREIGN KEY (user_id) REFERENCES users(id))")

    # select stocks and number of shares that user has purchased
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as sum FROM portfolio WHERE user_id = :user_id GROUP BY symbol ORDER BY symbol", user_id=session["user_id"])

    # initialise user stock total values
    stock_totals = 0.0

    # create list to store user's stocks
    user_stocks = []

    # iterate over each stock that user bought
    for stock in stocks:
        # dict to store individual stock
        stock_dict = {}
        quote = lookup(stock["symbol"])
        stock_dict["symbol"] = quote["symbol"]
        stock_dict["name"] = quote["name"]
        stock_dict["sum"] = int(stock["sum"])
        stock_dict["price"] = float(quote["price"])
        stock_dict["value"] = stock_dict["sum"] * stock_dict["price"]
        stock_totals = stock_totals + stock_dict["value"]

        # append each stock dict to list
        user_stocks.append(stock_dict)

    # calculate grand total for user
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    total_cash = float(cash[0]["cash"])
    total = total_cash + stock_totals

    return render_template("index.html", stocks=user_stocks, cash=total_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # make sure fields aren't left blank
        if not request.form.get("symbol"):
            return apology("Please enter a stock symbol", 400)

        # if shares left blank, ask for number of shares
        if not request.form.get("shares"):
            return apology("Please enter number of shares to purchase", 400)

        # if shares are not numeric, ask for a whole number
        if not request.form.get("shares").isdigit():
            return apology("Please enter a whole number", 400)

        quote = lookup(request.form.get("symbol"))

        # if stock symbol not found, return error and apologize
        if not quote:
            return apology("Stock could not be found", 400)

        # raises exception if user enters a negative number
        if int(request.form.get("shares")) <= 0:
            return apology("Please enter valid number of shares", 400)

        else:
            # selects user's current cash from users table
            can_has = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

            current_cash = can_has[0]["cash"]

            # calculate cost to purchase stock
            purchase = float(request.form.get("shares")) * quote["price"]

            # if user cannot afford stock, return apology
            if current_cash <= purchase:
                return apology("Insufficient funds", 400)

            # else, insert stock purchase data into user's portfolio table
            else:
                make_purchase = db.execute("INSERT INTO portfolio (user_id, symbol, name, shares, price, value, purchase_date) VALUES (:user_id, :symbol, :name, :shares, :price, :value, :purchase_date)",
                                           user_id=session["user_id"],
                                           symbol=quote["symbol"],
                                           name=quote["name"],
                                           shares=int(request.form.get("shares")),
                                           price=quote["price"],
                                           value=purchase,
                                           purchase_date=datetime.now())

                # complete purchase and charge user's account
                cost = current_cash - purchase
                payment = db.execute("UPDATE users SET cash = :cost WHERE id = :id", cost=cost, id=session["user_id"])

                flash("Bought!")
                return redirect("/")
    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # select stocks and number of shares that user has purchased
    stocks = db.execute("SELECT symbol, shares, name, price, purchase_date FROM portfolio WHERE user_id = :user_id",
                        user_id=session["user_id"])

    # create list to store user's stocks
    stock_history = []

    # iterate over each stock that user bought
    for stock in stocks:
        # dict to store individual stock
        stock_trans = {}
        stock_trans["symbol"] = stock["symbol"]
        stock_trans["name"] = stock["name"]
        stock_trans["shares"] = int(stock["shares"])
        stock_trans["price"] = float(stock["price"])
        stock_trans["date"] = stock["purchase_date"]
        if stock_trans["shares"] >= 1:
            stock_trans["action"] = "BUY"
        elif stock_trans["shares"] <= -1:
            stock_trans["action"] = "SELL"

        # append each stock dict to list
        stock_history.append(stock_trans)

    return render_template("history.html", stocks=stock_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        password = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(password) != 1 or not check_password_hash(password[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = password[0]["id"]

        # Redirect user to home page
        flash("Success!")
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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # lookup stock by symbol
        quote = lookup(request.form.get("symbol"))

        # make sure fields aren't left blank
        if not request.form.get("symbol"):
            return apology("Please enter a stock symbol", 400)

        # if stock symbol not found, return error and apologize
        elif not quote:
            return apology("stock could not be found", 400)

        # render html template for displaying stock price
        flash("Quoted!")
        return render_template("quoted.html", quoted=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # forget any user_id
    session.clear()

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # ensure password and confirmation fields match
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("password and confirmation must match", 400)

        # hash user's password
        hashed_password = generate_password_hash(request.form.get("password"))

        # insert user information into users table
        value_insert = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                                  username=request.form.get("username"), hash=hashed_password)

        # if username is already registered, apologize
        if not value_insert:
            return apology("username already exists", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # keep user logged in
        session["user_id"] = rows[0]["id"]
        flash("Registered!")
        return redirect("/")

    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("forgot_password.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # make sure fields aren't left blank
        if not request.form.get("symbol"):
            return apology("Please select a stock symbol to sell", 400)

        # if shares left blank, ask for number of shares
        if not request.form.get("shares"):
            return apology("Please enter number of shares to sell", 400)

        # if shares are not numeric, ask for a whole number
        if not request.form.get("shares").isdigit():
            return apology("Please enter a whole number", 400)

        quote = lookup(request.form.get("symbol"))

        # if stock symbol not found, return error and apologize
        if not quote:
            return apology("Stock could not be found", 400)

        # raises exception if user enters a negative number
        if int(request.form.get("shares")) <= 0:
            return apology("Please enter valid number of shares", 400)

        else:
            # selects user's current cash from users table
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            current_cash = cash[0]["cash"]

            user_shares = db.execute("SELECT SUM(shares) as sum_shares FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                                     user_id=session["user_id"], symbol=request.form.get("symbol"))

            if user_shares[0]["sum_shares"] < int(request.form.get("shares")):
                return apology("Not enough shares", 400)

            else:
                sell = float(request.form.get("shares")) * quote["price"]

                make_sale = db.execute("INSERT INTO portfolio (user_id, symbol, name, shares, price, value, purchase_date) VALUES (:user_id, :symbol, :name, :shares, :price, :value, :purchase_date)",
                                       user_id=session["user_id"],
                                       symbol=quote["symbol"],
                                       name=quote["name"],
                                       shares=int(request.form.get("shares")) * -1,
                                       price=quote["price"],
                                       value=sell,
                                       purchase_date=datetime.now())

                # complete purchase and charge user's account
                cost = current_cash + sell
                refund = db.execute("UPDATE users SET cash = :cost WHERE id = :id", cost=cost, id=session["user_id"])

                flash("Sold!")
                return redirect("/")

    else:
        # user reached route via GET (as by clicking a link or via redirect)
        stocks = db.execute("SELECT DISTINCT symbol FROM portfolio WHERE user_id = :user_id ORDER BY symbol",
                            user_id=session["user_id"])

        return render_template("sell.html", stocks=stocks)


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """change user password"""

    # forget any user_id
    session.clear()

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # ensure password and confirmation fields match
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("password and confirmation must match", 400)

        # hash user's new password
        hash_pass = generate_password_hash(request.form.get("password"))

        # update user's hashed password into users table
        new_pass = db.execute("UPDATE users SET hash = :hash WHERE username = :username",
                              username=request.form.get("username"), hash=hash_pass)

        # if username is already registered, apologize
        if not new_pass:
            return apology("username already exists", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # keep user logged in
        session["user_id"] = rows[0]["id"]
        flash("Password Changed!")
        return redirect("/")

    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("forgot_password.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)