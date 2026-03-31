from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))  # 'purchase', 'sale', 'balance'
    details = db.Column(db.String(200))

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)

# Initialize database and create tables
with app.app_context():
    db.create_all()
    # Ensure there is always one account row
    if Account.query.first() is None:
        db.session.add(Account(balance=10000))  # starting balance
        db.session.commit()

# --- HELPER FUNCTIONS ---
def get_balance():
    account = Account.query.first()
    return account.balance if account else 0

def set_balance(new_balance):
    account = Account.query.first()
    account.balance = new_balance
    db.session.commit()

def add_transaction(tx_type, details):
    try:
        tx = Transaction(type=tx_type, details=details)
        db.session.add(tx)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Database error:", e)

# --- ROUTES ---
@app.route("/")
def index():
    products = Product.query.all()
    balance = get_balance()
    warehouse = {p.name: p.quantity for p in products}
    return render_template("index.html", balance=balance, warehouse=warehouse)

@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == "POST":
        try:
            name = request.form["name"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            if price <= 0 or quantity <= 0:
                return "Invalid values"

            total = price * quantity
            balance = get_balance()
            if total > balance:
                return "Not enough balance"

            # Update balance
            set_balance(balance - total)

            # Update product stock
            product = Product.query.filter_by(name=name).first()
            if product:
                product.quantity += quantity
            else:
                product = Product(name=name, quantity=quantity)
                db.session.add(product)
            db.session.commit()

            add_transaction("purchase", f"{name}, {quantity} pcs at €{price}")
            return redirect(url_for("index"))
        except Exception as e:
            return f"Error: {e}"
    return render_template("purchase.html")

@app.route("/sale", methods=["GET", "POST"])
def sale():
    if request.method == "POST":
        try:
            name = request.form["name"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            product = Product.query.filter_by(name=name).first()
            if not product or product.quantity < quantity:
                return "Not enough stock"

            # Update stock and balance
            product.quantity -= quantity
            set_balance(get_balance() + price * quantity)
            db.session.commit()

            add_transaction("sale", f"{name}, {quantity} pcs at €{price}")
            return redirect(url_for("index"))
        except Exception as e:
            return f"Error: {e}"
    return render_template("sale.html")

@app.route("/balance", methods=["GET", "POST"])
def change_balance():
    if request.method == "POST":
        try:
            operation = request.form["operation"]
            amount = float(request.form["amount"])

            if amount <= 0:
                return "Invalid amount"

            balance = get_balance()
            if operation == "add":
                balance += amount
            elif operation == "subtract":
                if amount > balance:
                    return "Not enough balance"
                balance -= amount

            set_balance(balance)
            add_transaction("balance", f"{operation} €{amount}")
            return redirect(url_for("index"))
        except Exception as e:
            return f"Error: {e}"
    return render_template("balance.html")

@app.route("/history/")
@app.route("/history/<int:line_from>/<int:line_to>/")
def show_history(line_from=None, line_to=None):
    transactions = Transaction.query.order_by(Transaction.id).all()
    if line_from is not None and line_to is not None:
        transactions = transactions[line_from:line_to]
    return render_template("history.html", history=transactions)

if __name__ == "__main__":
    app.run(debug=True)