# Design a robust Inventory Management System in Python that can manage different types of products, handle stock operations,
#  sales, and persist data. This challenge is meant to polish your OOP concepts and make you confident in applying them in real-world use cases.


import json
from abc import ABC, abstractmethod
from datetime import datetime


# ---------------- Custom Exceptions ----------------
class DuplicateProductIDError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InvalidProductDataError(Exception):
    pass


# ---------------- Abstract Product Class ----------------
class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity

    @abstractmethod
    def __str__(self):
        pass

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(f"Only {self._quantity_in_stock} items left in stock.")
        self._quantity_in_stock -= quantity

    def get_total_value(self):
        return self._price * self._quantity_in_stock

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity": self._quantity_in_stock
        }


# ---------------- Electronics ----------------
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity, brand, warranty_years):
        super().__init__(product_id, name, price, quantity)
        self._brand = brand
        self._warranty_years = warranty_years

    def __str__(self):
        return f"[Electronics] {self._name} (ID: {self._product_id}, Brand: {self._brand}, Warranty: {self._warranty_years} yrs, Price: ${self._price}, Stock: {self._quantity_in_stock})"

    def to_dict(self):
        data = super().to_dict()
        data.update({"brand": self._brand, "warranty_years": self._warranty_years})
        return data


# ---------------- Grocery ----------------
class Grocery(Product):
    def __init__(self, product_id, name, price, quantity, expiry_date):
        super().__init__(product_id, name, price, quantity)
        self._expiry_date = expiry_date  # format: YYYY-MM-DD

    def is_expired(self):
        today = datetime.today().date()
        return today > datetime.strptime(self._expiry_date, "%Y-%m-%d").date()

    def __str__(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return f"[Grocery] {self._name} (ID: {self._product_id}, Expiry: {self._expiry_date}, Status: {status}, Price: ${self._price}, Stock: {self._quantity_in_stock})"

    def to_dict(self):
        data = super().to_dict()
        data.update({"expiry_date": self._expiry_date})
        return data


# ---------------- Clothing ----------------
class Clothing(Product):
    def __init__(self, product_id, name, price, quantity, size, material):
        super().__init__(product_id, name, price, quantity)
        self._size = size
        self._material = material

    def __str__(self):
        return f"[Clothing] {self._name} (ID: {self._product_id}, Size: {self._size}, Material: {self._material}, Price: ${self._price}, Stock: {self._quantity_in_stock})"

    def to_dict(self):
        data = super().to_dict()
        data.update({"size": self._size, "material": self._material})
        return data


# ---------------- Inventory Class ----------------
class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product._product_id in self._products:
            raise DuplicateProductIDError("Product ID already exists.")
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        self._products.pop(product_id, None)

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__.lower() == product_type.lower()]

    def list_all_products(self):
        return list(self._products.values())

    def sell_product(self, product_id, quantity):
        if product_id in self._products:
            self._products[product_id].sell(quantity)

    def restock_product(self, product_id, quantity):
        if product_id in self._products:
            self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        expired_ids = [pid for pid, p in self._products.items() if isinstance(p, Grocery) and p.is_expired()]
        for pid in expired_ids:
            del self._products[pid]

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump([p.to_dict() for p in self._products.values()], f, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    ptype = item['type']
                    if ptype == "Electronics":
                        product = Electronics(item['product_id'], item['name'], item['price'], item['quantity'], item['brand'], item['warranty_years'])
                    elif ptype == "Grocery":
                        product = Grocery(item['product_id'], item['name'], item['price'], item['quantity'], item['expiry_date'])
                    elif ptype == "Clothing":
                        product = Clothing(item['product_id'], item['name'], item['price'], item['quantity'], item['size'], item['material'])
                    else:
                        raise InvalidProductDataError("Unknown product type.")
                    self.add_product(product)
        except FileNotFoundError:
            print("File not found.")


# ---------------- CLI Interface ----------------
def menu():
    inv = Inventory()
    while True:
        print("\n------ Inventory Menu ------")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. View All Products")
        print("5. Search Product by Name")
        print("6. Search Product by Type")
        print("7. Remove Expired Groceries")
        print("8. Total Inventory Value")
        print("9. Save Inventory to File")
        print("10. Load Inventory from File")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                ptype = input("Type (electronics/grocery/clothing): ").lower()
                pid = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                qty = int(input("Quantity: "))

                if ptype == "electronics":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty (years): "))
                    product = Electronics(pid, name, price, qty, brand, warranty)

                elif ptype == "grocery":
                    expiry = input("Expiry Date (YYYY-MM-DD): ")
                    product = Grocery(pid, name, price, qty, expiry)

                elif ptype == "clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = Clothing(pid, name, price, qty, size, material)

                else:
                    print("Invalid product type.")
                    continue

                inv.add_product(product)
                print("Product added successfully.")

            elif choice == "2":
                pid = input("Product ID: ")
                qty = int(input("Quantity to sell: "))
                inv.sell_product(pid, qty)
                print("Product sold successfully.")

            elif choice == "3":
                pid = input("Product ID: ")
                qty = int(input("Quantity to restock: "))
                inv.restock_product(pid, qty)
                print("Product restocked successfully.")

            elif choice == "4":
                for p in inv.list_all_products():
                    print(p)

            elif choice == "5":
                name = input("Enter name to search: ")
                results = inv.search_by_name(name)
                for p in results:
                    print(p)

            elif choice == "6":
                ptype = input("Enter product type: ")
                results = inv.search_by_type(ptype)
                for p in results:
                    print(p)

            elif choice == "7":
                inv.remove_expired_products()
                print("Expired grocery products removed.")

            elif choice == "8":
                print(f"Total Inventory Value: ${inv.total_inventory_value()}")

            elif choice == "9":
                inv.save_to_file("inventory_data.json")
                print("Inventory saved to file.")

            elif choice == "10":
                inv.load_from_file("inventory_data.json")
                print("Inventory loaded from file.")

            elif choice == "0":
                print("Exiting system.")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print("Error:", e)


# ---------------- Entry Point ----------------
if __name__ == "__main__":
    menu()