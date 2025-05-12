# 🛒 Inventory Management System (Python OOP Project)

## 📌 Overview

This project is an **Advanced Object-Oriented Programming (OOP)** challenge implemented in Python. It simulates a robust **Inventory Management System** capable of managing various product types (Electronics, Grocery, Clothing), performing operations like restocking, selling, and calculating stock value — all while persisting data using JSON files.

---

## 🎯 Objectives

- Apply **abstract base classes** and **inheritance**
- Implement **encapsulation**, **polymorphism**, and **custom exceptions**
- Use **JSON serialization/deserialization** for file operations
- Design a **CLI menu system** for user interaction

---

## 🧱 Project Structure

### 🔹 `Product (Abstract Class)`
Defines a blueprint for all product types using `abc` module.

**Attributes (Encapsulated):**
- `_product_id`
- `_name`
- `_price`
- `_quantity_in_stock`

**Key Methods:**
- `restock(amount)`
- `sell(quantity)`
- `get_total_value()`
- `__str__()` → Overridden in subclasses

---

### 🔹 Product Subclasses

#### 1. `Electronics`
- Extra Attributes: `brand`, `warranty_years`

#### 2. `Grocery`
- Extra Attribute: `expiry_date`
- Method: `is_expired()`

#### 3. `Clothing`
- Extra Attributes: `size`, `material`

Each subclass overrides `__str__()` to show product-specific information.

---

### 🔹 `Inventory` Class

Manages all products in a dictionary and provides operations like:
- `add_product()`
- `remove_product()`
- `search_by_name()`
- `search_by_type()`
- `sell_product()`
- `restock_product()`
- `remove_expired_products()` (specific to `Grocery`)
- `save_to_file()`, `load_from_file()` (JSON persistence)
- `total_inventory_value()`

---

### ⚠️ Custom Exceptions

- `DuplicateProductIDError` – Prevents duplicate entries
- `InsufficientStockError` – Raised if trying to sell more than available
- `InvalidProductDataError` – Handles corrupted/invalid JSON product data

---

### 🖥️ CLI Menu Features

Interactive menu loop to:
- Add new products
- Sell/restock inventory
- View/search products
- Save/load inventory from `inventory_data.json`
- Remove expired grocery items
- Exit the system

---

## 🏁 Getting Started

### ▶️ How to Run:

```bash
python inventory.py
