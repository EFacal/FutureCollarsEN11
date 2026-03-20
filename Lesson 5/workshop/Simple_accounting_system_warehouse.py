balance = 0
warehouse = {}
operations = []

print("Available commands:")
print("balance")
print("sale")
print("purchase")
print("account")
print("list")
print("warehouse")
print("review")
print("end")

while True:
    command = input("Enter command: ")

    # -------- BALANCE --------
    if command == "balance":
        amount = float(input("Enter amount to add or subtract: "))
        balance = balance + amount
        operations.append("BALANCE: {}".format(amount))
        print("Current balance:", balance)

    # -------- SALE --------
    elif command == "sale":
        name = input("Product name: ")
        price = float(input("Product price: "))
        quantity = int(input("Quantity: "))

        if name in warehouse and warehouse[name]["quantity"] >= quantity:
            total = price * quantity
            balance = balance + total
            warehouse[name]["quantity"] = warehouse[name]["quantity"] - quantity

            operations.append(
                "SALE: {}, qty={}, total={}".format(name, quantity, total)
            )
            print("Sale completed.")
        else:
            print("Not enough product in warehouse.")

    # -------- PURCHASE --------
    elif command == "purchase":
        name = input("Product name: ")
        price = float(input("Product price: "))
        quantity = int(input("Quantity: "))

        total = price * quantity

        if balance >= total:
            balance = balance - total

            if name in warehouse:
                warehouse[name]["quantity"] = warehouse[name]["quantity"] + quantity
                warehouse[name]["price"] = price
            else:
                warehouse[name] = {
                    "price": price,
                    "quantity": quantity
                }

            operations.append(
                "PURCHASE: {}, qty={}, total={}".format(name, quantity, total)
            )
            print("Purchase completed.")
        else:
            print("Not enough money.")

    # -------- ACCOUNT --------
    elif command == "account":
        print("Current balance:", balance)

    # -------- LIST --------
    elif command == "list":
        if not warehouse:
            print("Warehouse is empty.")
        else:
            for product in warehouse:
                print(
                    product,
                    "price:",
                    warehouse[product]["price"],
                    "quantity:",
                    warehouse[product]["quantity"]
                )

    # -------- WAREHOUSE --------
    elif command == "warehouse":
        name = input("Enter product name: ")
        if name in warehouse:
            print(
                name,
                "price:",
                warehouse[name]["price"],
                "quantity:",
                warehouse[name]["quantity"]
            )
        else:
            print("Product not found.")

    # -------- REVIEW --------
    elif command == "review":
        start = input("From index (Enter for all): ")
        end = input("To index (Enter for all): ")

        if start == "" and end == "":
            for op in operations:
                print(op)
        else:
            start = int(start)
            end = int(end)

            if start < 0 or end > len(operations):
                print("Index out of range.")
            else:
                for i in range(start, end):
                    print(operations[i])

    # -------- END --------
    elif command == "end":
        print("Program ended.")
        break

    # -------- UNKNOWN --------
    else:
        print("Unknown command.")

    print()
    print("Available commands:")
    print("balance")
    print("sale")
    print("purchase")
    print("account")
    print("list")
    print("warehouse")
    print("review")
    print("end")