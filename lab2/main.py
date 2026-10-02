import os
import json
from pymongo import MongoClient

# підключаємось до локальної монги
client = MongoClient("mongodb://localhost:27017/")
db = client["techstore"]

docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_docs")

# зчитуємо документи для каталогу товарів
products = []
for i in range(1, 4):
    file_path = os.path.join(docs_dir, f"product_{i}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        products.append(json.load(f))

# зчитуємо документи замовлень
orders = []
for i in range(1, 4):
    file_path = os.path.join(docs_dir, f"order_{i}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        orders.append(json.load(f))

# очищаєм старі дані перед вставкою
db.products.drop()
db.orders.drop()

# закидаєм нові документи
res_prod = db.products.insert_many(products)
res_ord = db.orders.insert_many(orders)

print("Products inserted:", len(res_prod.inserted_ids))
print("Orders inserted:", len(res_ord.inserted_ids))

# виводимо товари з масивами і вкладеними документами
print("\n--- Products in database ---")
for p in db.products.find():
    name = p.get("name")
    price = p.get("price")
    print(f"- {name}: {price} UAH")
    if "specifications" in p:
        print("  specs:", p["specifications"])
    if "tags" in p:
        print("  tags:", p["tags"])

# виводимо замовлення
print("\n--- Orders in database ---")
for o in db.orders.find():
    oid = o.get("order_id")
    total = o.get("total_amount")
    print(f"- Order {oid}: total {total} UAH")
    if "delivery_details" in o:
        print("  delivery:", o["delivery_details"]["city"], o["delivery_details"]["courier_service"])
    if "items" in o:
        print(f"  items count: {len(o['items'])}")
