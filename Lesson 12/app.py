from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

balance = 0
warehouse = {}
history = []

HISTORY_FILE = "history.txt"


# -------- FILE HANDLING --------
def load_history():
    global history
    try:
        with open(HISTORY_FILE, "r") as f:
            history = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        history = []


def save_history(entry):
    try:
        with open(HISTORY_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception:
        print("Error writing to file")


load_history()


# -------- ROUTES --------

@app.route("/")
def index():
    return render_template("index.html", balance=balance, warehouse=warehouse)


@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    global balance

    if request.method == "POST":
        try:
            name = request.form["name"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            if price <= 0 or quantity <= 0:
                return "Invalid values"

            total = price * quantity

            if total > balance:
                return "Not enough balance"

            balance -= total
            warehouse[name] = warehouse.get(name, 0) + quantity

            entry = f"Purchase: {name}, {quantity}, {price}"
            history.append(entry)
            save_history(entry)

            return redirect(url_for("index"))

        except:
            return "Invalid input"

    return render_template("purchase.html")


@app.route("/sale", methods=["GET", "POST"])
def sale():
    global balance

    if request.method == "POST":
        try:
            name = request.form["name"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            if name not in warehouse or warehouse[name] < quantity:
                return "Not enough stock"

            balance += price * quantity
            warehouse[name] -= quantity

            entry = f"Sale: {name}, {quantity}, {price}"
            history.append(entry)
            save_history(entry)

            return redirect(url_for("index"))

        except:
            return "Invalid input"

    return render_template("sale.html")


@app.route("/balance", methods=["GET", "POST"])
def change_balance():
    global balance

    if request.method == "POST":
        try:
            operation = request.form["operation"]
            amount = float(request.form["amount"])

            if amount <= 0:
                return "Invalid amount"

            if operation == "add":
                balance += amount
            elif operation == "subtract":
                if amount > balance:
                    return "Not enough balance"
                balance -= amount

            entry = f"Balance: {operation} {amount}"
            history.append(entry)
            save_history(entry)

            return redirect(url_for("index"))

        except:
            return "Invalid input"

    return render_template("balance.html")


@app.route("/history/")
@app.route("/history/<int:line_from>/<int:line_to>/")
def show_history(line_from=None, line_to=None):

    if line_from is None or line_to is None:
        filtered = history
    else:
        filtered = history[line_from:line_to]

    return render_template("history.html", history=filtered)


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)