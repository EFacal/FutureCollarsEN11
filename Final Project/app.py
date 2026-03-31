from flask import Flask, render_template, request, redirect
from models import db, Product, Transaction
from services import InventoryService, BalanceService
from decorators import validate_form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    products = Product.query.all()
    balance = sum(t.amount for t in Transaction.query.all())
    return render_template("index.html", products=products, balance=balance)


@app.route("/purchase", methods=["GET", "POST"])
@validate_form(["name", "price", "quantity"])
def purchase():
    if request.method == "POST":
        try:
            InventoryService.purchase(
                request.form["name"],
                float(request.form["price"]),
                int(request.form["quantity"])
            )
            return redirect("/")
        except Exception as e:
            return str(e)
    return render_template("purchase.html")


@app.route("/sale", methods=["GET", "POST"])
@validate_form(["name", "price", "quantity"])
def sale():
    if request.method == "POST":
        try:
            InventoryService.sale(
                request.form["name"],
                float(request.form["price"]),
                int(request.form["quantity"])
            )
            return redirect("/")
        except Exception as e:
            return str(e)
    return render_template("sale.html")


@app.route("/balance", methods=["GET", "POST"])
@validate_form(["operation", "amount"])
def balance():
    if request.method == "POST":
        try:
            BalanceService.change(
                request.form["operation"],
                float(request.form["amount"])
            )
            return redirect("/")
        except Exception as e:
            return str(e)
    return render_template("balance.html")


@app.route("/history/")
@app.route("/history/<int:start>/<int:end>/")
def history(start=None, end=None):
    transactions = Transaction.query.all()

    if start is not None and end is not None:
        transactions = transactions[start:end]

    return render_template("history.html", transactions=transactions)


@app.route("/stats")
def stats():
    transactions = Transaction.query.all()

    total_purchase = sum(-t.amount for t in transactions if t.type == "purchase")
    total_sales = sum(t.amount for t in transactions if t.type == "sale")

    product_sales = {}
    for t in transactions:
        if t.type == "sale":
            product_sales[t.product_name] = product_sales.get(t.product_name, 0) + t.quantity

    most_sold = max(product_sales, key=product_sales.get) if product_sales else "N/A"

    return render_template(
        "stats.html",
        total_purchase=total_purchase,
        total_sales=total_sales,
        most_sold=most_sold
    )


if __name__ == "__main__":
    app.run(debug=True)