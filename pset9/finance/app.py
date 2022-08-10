
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userid = session["user_id"]
    holdings = db.execute("SELECT * FROM holdings WHERE userid = ?", userid)

    data = db.execute("SELECT * FROM purchase WHERE userid = ?", userid)
    cashq = db.execute("SELECT cash FROM users WHERE id = ?", userid)
    current_price = {}
    total = {}
    if (len(cashq) < 1):
        cash = 10000
    else:
        cash = cashq[0]["cash"]
    gtotal = cash
    for dic in data:
        current_price[dic["symbol"]] = lookup(dic["symbol"])["price"]
        total[dic["symbol"]] = lookup(dic["symbol"])["price"] * dic["quantity"]
        gtotal += total[dic["symbol"]]

    return render_template("index.html", cash=cash, current_price=current_price, total=total, gtotal=gtotal, data=data, holdings=holdings)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # amount for total shares
        data = lookup(symbol)

        if not symbol or not shares:
            return apology("Required number of Shares.")
        elif data == None:
            return apology("Invalid Stock Symbol")

        try:
            shares = int(shares)
        except:
            return apology("Invalid no of shares")

        if shares < 0:
            return apology('Cant buy negative Shares')
        stock_price = lookup(symbol)["price"]
        amount = shares * stock_price
        stock_name = lookup(symbol)["name"]
        # checking for balance
        userid = session["user_id"]
        balance_db = db.execute("SELECT cash FROM users WHERE id = ? ", userid)
        user_cash = balance_db[0]['cash']

        # evaluating for sufficient balance
        if user_cash < amount:
            return apology("Insufficient Balance to buy stocks")

        update_cash = user_cash-amount

        day = date.today().strftime("%B %d, %Y")
        type = "buy"

        db.execute("UPDATE users SET cash=? WHERE id=? ", update_cash, userid)
        db.execute("INSERT INTO purchase (userid ,symbol,name,price,quantity,date,type) VALUES(?,?,?,?,?,?,?)",
                   userid, symbol, stock_name, stock_price, shares, day, type)
        db.execute("INSERT INTO holdings (userid ,symbol,quantity) VALUES(?,?,?)",
                   userid, symbol, shares)
        flash("Bought!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute("SELECT * FROM purchase WHERE userid = ?", session["user_id"])
    return render_template("history.html", data=data)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        stock = request.form.get("symbol")
        data = lookup(stock)
        if data != None:
            return render_template("quoted.html", data=data)
        else:
            return apology("Invalid Stock Symbol")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        # Ensure password was submitted
        elif not password:
            return apology("must provide password")
         # Ensure confirm password was submitted
        elif not confirm_password:
            return apology("must provide confirm password")
         # Ensure password and confirm passsword match
        elif password != confirm_password:
            return apology("passwords don't match")
        # checking for unique username
        rows = db.execute("SELECT * FROM users")

        for dicts in rows:
            if dicts["username"] == username:
                return apology("choose unique username")

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)",
                   username, hash)
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        query = db.execute("SELECT symbol,quantity FROM purchase WHERE userid=:userid", userid=session["user_id"])
        return render_template("sell.html", query=query)
    else:
        userid = session["user_id"]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        cash = db.execute("SELECT cash FROM users WHERE id=?", userid)[0]["cash"]

        quantity = db.execute("SELECT quantity FROM purchase WHERE userid=? AND symbol= ?", userid, symbol)[0]["quantity"]

        if symbol == None:
            return apology("Symbol required")

        elif lookup(symbol) == None:
            return apology("Invalid symbol")

        elif shares == None:
            return apology("Incomplete input")

        elif int(shares) > quantity:
            return apology("Not enough shares")

        shares = int(shares)

        cprice = int(lookup(symbol)["price"])
        name = lookup(symbol)["name"]
        amount = cprice * shares

        update_cash = cash + amount
        update_quantity = quantity - shares

        day = date.today().strftime("%B %d, %Y")
        type = "sold"

        db.execute("UPDATE users SET cash=? WHERE id=? ", update_cash, userid)
        db.execute("INSERT INTO purchase (userid ,symbol,name,price,quantity,date,type) VALUES(?,?,?,?,?,?,?)",
                   userid, symbol, name, cprice, shares, day, type)
        db.execute("UPDATE holdings SET quantity = ? WHERE userid = ? AND symbol = ? ", update_quantity, userid, symbol)

        check = db.execute("SELECT quantity FROM holdings WHERE userid = ? AND symbol = ? ", userid, symbol)[0]["quantity"]
        if (check <= 0):
            db.execute("DELETE FROM holdings WHERE userid = ? AND symbol = ? ", userid, symbol)
        flash("sold!")
        return redirect("/")

