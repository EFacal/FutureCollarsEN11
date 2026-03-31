from models import db, Product, Transaction


class InventoryService:

    @staticmethod
    def purchase(name, price, quantity):
        product = Product.query.filter_by(name=name).first()

        if not product:
            product = Product(name=name, quantity=0)
            db.session.add(product)

        product.quantity += quantity

        transaction = Transaction(
            type="purchase",
            product_name=name,
            quantity=quantity,
            price=price,
            amount=-(price * quantity)
        )

        db.session.add(transaction)
        db.session.commit()

    @staticmethod
    def sale(name, price, quantity):
        product = Product.query.filter_by(name=name).first()

        if not product or product.quantity < quantity:
            raise ValueError("Not enough stock")

        product.quantity -= quantity

        transaction = Transaction(
            type="sale",
            product_name=name,
            quantity=quantity,
            price=price,
            amount=(price * quantity)
        )

        db.session.add(transaction)
        db.session.commit()


class BalanceService:

    @staticmethod
    def change(operation, amount):
        if operation not in ["add", "subtract"]:
            raise ValueError("Invalid operation")

        amount = amount if operation == "add" else -amount

        transaction = Transaction(
            type="balance",
            amount=amount
        )

        db.session.add(transaction)
        db.session.commit()