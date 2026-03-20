import os
from ast import literal_eval
import Simple_accounting_system_warehouse

FILENAME = "data.txt"

balance = 0
warehouse = {}
operations = []

# -------- LOAD DATA --------
if os.path.exists(FILENAME):
    try:
        with open(FILENAME, "r") as file:
            data = literal_eval(file.read())
            balance = data.get("balance", 0)
            warehouse = data.get("warehouse", {})
            operations = data.get("operations", [])
        print("Data loaded successfully.")
    except (ValueError, SyntaxError, OSError):
        print("Error reading file. Starting with empty data.")
else:
    print("No saved file found. Starting fresh.")

# -------- RUN SYSTEM --------
balance, warehouse, operations = Simple_accounting_system.run(
    balance, warehouse, operations
)

# -------- SAVE DATA --------
try:
    with open(FILENAME, "w") as file:
        data = {
            "balance": balance,
            "warehouse": warehouse,
            "operations": operations
        }
        file.write(str(data))
    print("Data saved successfully.")
except OSError:
    print("Error saving data.")