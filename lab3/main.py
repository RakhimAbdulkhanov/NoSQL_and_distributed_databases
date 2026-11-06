import datetime
from bson import ObjectId
from pymongo import MongoClient

# підключаємось до локального інстансу монго
client = MongoClient("mongodb://localhost:27017/")
db = client["techstore"]

# скидаємо старі колекції перед запуском
db.products.drop()
db.customers.drop()
db.orders.drop()

# список товарів (10 документів, кожен містить різні типи BSON)
products_data = [
    {
        "name": "Процесор AMD Ryzen 7 7800X3D",
        "category": "Процесори",
        "price": 18499.0,
        "in_stock": True,
        "stock_quantity": 25,
        "tags": ["cpu", "am5", "gaming", "v-cache"],
        "specifications": {
            "socket": "AM5",
            "cores": 8,
            "threads": 16,
            "base_clock_ghz": 4.2,
            "tdp_watts": 120,
            "ram_type": "DDR5"
        }
    },
    {
        "name": "Процесор Intel Core i7-14700K",
        "category": "Процесори",
        "price": 17299.0,
        "in_stock": True,
        "stock_quantity": 18,
        "tags": ["cpu", "lga1700", "raptor-lake"],
        "specifications": {
            "socket": "LGA1700",
            "cores": 20,
            "threads": 28,
            "base_clock_ghz": 3.4,
            "tdp_watts": 125,
            "ram_type": "DDR5"
        }
    },
    {
        "name": "Відеокарта ASUS ROG Strix GeForce RTX 4080 Super",
        "category": "Відеокарти",
        "price": 49999.0,
        "in_stock": True,
        "stock_quantity": 7,
        "tags": ["gpu", "nvidia", "rtx", "4k-gaming"],
        "specifications": {
            "vram_gb": 16,
            "bus_width_bit": 256,
            "interface": "PCI-e 4.0",
            "recommended_psu_watts": 750
        }
    },
    {
        "name": "Відеокарта Sapphire Nitro+ Radeon RX 7900 XTX",
        "category": "Відеокарти",
        "price": 43500.0,
        "in_stock": False,
        "stock_quantity": 0,
        "tags": ["gpu", "amd", "radeon", "rdna3"],
        "specifications": {
            "vram_gb": 24,
            "bus_width_bit": 384,
            "interface": "PCI-e 4.0",
            "recommended_psu_watts": 800
        }
    },
    {
        "name": "Материнська плата MSI MAG B650 TOMAHAWK WIFI",
        "category": "Материнські плати",
        "price": 8999.0,
        "in_stock": True,
        "stock_quantity": 14,
        "tags": ["motherboard", "am5", "wifi6e", "atx"],
        "specifications": {
            "socket": "AM5",
            "form_factor": "ATX",
            "ram_slots": 4,
            "max_ram_gb": 192,
            "ram_type": "DDR5"
        }
    },
    {
        "name": "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000",
        "category": "Оперативна пам'ять",
        "price": 5499.0,
        "in_stock": True,
        "stock_quantity": 30,
        "tags": ["ram", "ddr5", "cl32", "rgb"],
        "specifications": {
            "capacity_gb": 32,
            "ram_type": "DDR5",
            "frequency_mhz": 6000,
            "kit": "2x16GB",
            "voltage": 1.35
        }
    },
    {
        "name": "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe",
        "category": "Накопичувачі",
        "price": 7899.0,
        "in_stock": True,
        "stock_quantity": 22,
        "tags": ["ssd", "nvme", "pcie4", "m2"],
        "specifications": {
            "form_factor": "M.2 2280",
            "capacity_gb": 2000,
            "read_speed_mb": 7450,
            "write_speed_mb": 6900
        }
    },
    {
        "name": "Блок живлення Seasonic Focus GX-850 850W Gold",
        "category": "Блоки живлення",
        "price": 6299.0,
        "in_stock": True,
        "stock_quantity": 12,
        "tags": ["psu", "modular", "80plus-gold"],
        "specifications": {
            "power_watts": 850,
            "efficiency": "80 PLUS Gold",
            "modular": "full",
            "fan_size_mm": 120
        }
    },
    {
        "name": "Корпус Fractal Design North Charcoal Black",
        "category": "Корпуси",
        "price": 6899.0,
        "in_stock": True,
        "stock_quantity": 9,
        "tags": ["case", "mid-tower", "wood-front", "mesh"],
        "specifications": {
            "form_factor": "Mid-Tower",
            "supported_motherboards": ["ATX", "Micro-ATX", "Mini-ITX"],
            "gpu_max_length_mm": 355
        }
    },
    {
        "name": "Ігровий монітор ASUS TUF Gaming VG27AQ",
        "category": "Монітори",
        "price": 13999.0,
        "in_stock": True,
        "stock_quantity": 15,
        "tags": ["monitor", "2k", "ips", "165hz", "g-sync"],
        "specifications": {
            "diagonal_inch": 27.0,
            "resolution": "2560x1440",
            "matrix": "IPS",
            "refresh_rate_hz": 165
        }
    }
]

# список клієнтів (10 документів з вкладеними адресами)
customers_data = [
    {
        "customer_code": "CUST-001",
        "name": "Олександр Мельник",
        "email": "o.melnyk@gmail.com",
        "phone": "+380501112233",
        "loyalty_level": "gold",
        "discount_pct": 10,
        "address": {
            "city": "Львів",
            "street": "вул. Франка, 15",
            "apartment": 4,
            "zip": "79005"
        }
    },
    {
        "customer_code": "CUST-002",
        "name": "Ірина Ковальчук",
        "email": "i.koval@ukr.net",
        "phone": "+380672223344",
        "loyalty_level": "silver",
        "discount_pct": 5,
        "address": {
            "city": "Київ",
            "street": "просп. Перемоги, 42",
            "apartment": 128,
            "zip": "03057"
        }
    },
    {
        "customer_code": "CUST-003",
        "name": "Максим Шевченко",
        "email": "m.sheva@tech.io",
        "phone": "+380933334455",
        "loyalty_level": "platinum",
        "discount_pct": 15,
        "address": {
            "city": "Львів",
            "street": "вул. Городоцька, 110",
            "apartment": 22,
            "zip": "79018"
        }
    },
    {
        "customer_code": "CUST-004",
        "name": "Анна Бондаренко",
        "email": "a.bond@outlook.com",
        "phone": "+380634445566",
        "loyalty_level": "standard",
        "discount_pct": 0,
        "address": {
            "city": "Харків",
            "street": "вул. Сумська, 5",
            "apartment": 18,
            "zip": "61057"
        }
    },
    {
        "customer_code": "CUST-005",
        "name": "Тарас Романюк",
        "email": "t.romanyuk@gmail.com",
        "phone": "+380975556677",
        "loyalty_level": "gold",
        "discount_pct": 10,
        "address": {
            "city": "Івано-Франківськ",
            "street": "вул. Незалежності, 73",
            "apartment": 9,
            "zip": "76018"
        }
    },
    {
        "customer_code": "CUST-006",
        "name": "Дмитро Сидоренко",
        "email": "d.sydor@meta.ua",
        "phone": "+380506667788",
        "loyalty_level": "silver",
        "discount_pct": 5,
        "address": {
            "city": "Дніпро",
            "street": "просп. Яворницького, 18",
            "apartment": 55,
            "zip": "49000"
        }
    },
    {
        "customer_code": "CUST-007",
        "name": "Олена Василенко",
        "email": "olena.v@yahoo.com",
        "phone": "+380677778899",
        "loyalty_level": "standard",
        "discount_pct": 0,
        "address": {
            "city": "Львів",
            "street": "вул. Стрийська, 85",
            "apartment": 64,
            "zip": "79031"
        }
    },
    {
        "customer_code": "CUST-008",
        "name": "Андрій Ткачук",
        "email": "a.tkachuk@gmail.com",
        "phone": "+380938889900",
        "loyalty_level": "gold",
        "discount_pct": 10,
        "address": {
            "city": "Тернопіль",
            "street": "вул. Руська, 12",
            "apartment": 3,
            "zip": "46001"
        }
    },
    {
        "customer_code": "CUST-009",
        "name": "Вікторія Мороз",
        "email": "v.moroz@icloud.com",
        "phone": "+380991234567",
        "loyalty_level": "platinum",
        "discount_pct": 15,
        "address": {
            "city": "Київ",
            "street": "вул. Хрещатик, 24",
            "apartment": 30,
            "zip": "01001"
        }
    },
    {
        "customer_code": "CUST-010",
        "name": "Сергій Кравченко",
        "email": "s.kravch@ukr.net",
        "phone": "+380967654321",
        "loyalty_level": "silver",
        "discount_pct": 5,
        "address": {
            "city": "Одеса",
            "street": "вул. Дерибасівська, 9",
            "apartment": 15,
            "zip": "65026"
        }
    }
]

# заповнюємо колекції товарів та клієнтів
res_prod = db.products.insert_many(products_data)
res_cust = db.customers.insert_many(customers_data)

prod_ids = res_prod.inserted_ids
cust_ids = res_cust.inserted_ids

# словники для швидкого пошуку id за назвою / кодом
prod_map = {p["name"]: pid for p, pid in zip(products_data, prod_ids)}
cust_map = {c["customer_code"]: cid for c, cid in zip(customers_data, cust_ids)}

# список замовлень із посиланнями на клієнтів (ObjectId) та вкладеними товарами
orders_data = [
    {
        "order_number": "ORD-2026-101",
        "customer_id": cust_map["CUST-001"],
        "order_date": datetime.datetime(2026, 3, 10, 11, 30),
        "status": "completed",
        "payment_method": "card",
        "total_amount": 27498.0,
        "items": [
            {
                "product_id": prod_map["Процесор AMD Ryzen 7 7800X3D"],
                "name": "Процесор AMD Ryzen 7 7800X3D",
                "quantity": 1,
                "unit_price": 18499.0
            },
            {
                "product_id": prod_map["Материнська плата MSI MAG B650 TOMAHAWK WIFI"],
                "name": "Материнська плата MSI MAG B650 TOMAHAWK WIFI",
                "quantity": 1,
                "unit_price": 8999.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-102",
        "customer_id": cust_map["CUST-003"],
        "order_date": datetime.datetime(2026, 3, 11, 14, 15),
        "status": "completed",
        "payment_method": "bank_transfer",
        "total_amount": 49999.0,
        "items": [
            {
                "product_id": prod_map["Відеокарта ASUS ROG Strix GeForce RTX 4080 Super"],
                "name": "Відеокарта ASUS ROG Strix GeForce RTX 4080 Super",
                "quantity": 1,
                "unit_price": 49999.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-103",
        "customer_id": cust_map["CUST-002"],
        "order_date": datetime.datetime(2026, 3, 12, 16, 40),
        "status": "completed",
        "payment_method": "card",
        "total_amount": 13398.0,
        "items": [
            {
                "product_id": prod_map["Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000"],
                "name": "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000",
                "quantity": 1,
                "unit_price": 5499.0
            },
            {
                "product_id": prod_map["SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe"],
                "name": "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe",
                "quantity": 1,
                "unit_price": 7899.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-104",
        "customer_id": cust_map["CUST-005"],
        "order_date": datetime.datetime(2026, 3, 14, 10, 5),
        "status": "processing",
        "payment_method": "cash_on_delivery",
        "total_amount": 13198.0,
        "items": [
            {
                "product_id": prod_map["Блок живлення Seasonic Focus GX-850 850W Gold"],
                "name": "Блок живлення Seasonic Focus GX-850 850W Gold",
                "quantity": 1,
                "unit_price": 6299.0
            },
            {
                "product_id": prod_map["Корпус Fractal Design North Charcoal Black"],
                "name": "Корпус Fractal Design North Charcoal Black",
                "quantity": 1,
                "unit_price": 6899.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-105",
        "customer_id": cust_map["CUST-007"],
        "order_date": datetime.datetime(2026, 3, 15, 12, 50),
        "status": "shipped",
        "payment_method": "card",
        "total_amount": 13999.0,
        "items": [
            {
                "product_id": prod_map["Ігровий монітор ASUS TUF Gaming VG27AQ"],
                "name": "Ігровий монітор ASUS TUF Gaming VG27AQ",
                "quantity": 1,
                "unit_price": 13999.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-106",
        "customer_id": cust_map["CUST-009"],
        "order_date": datetime.datetime(2026, 3, 16, 9, 20),
        "status": "completed",
        "payment_method": "bank_transfer",
        "total_amount": 31298.0,
        "items": [
            {
                "product_id": prod_map["Процесор Intel Core i7-14700K"],
                "name": "Процесор Intel Core i7-14700K",
                "quantity": 1,
                "unit_price": 17299.0
            },
            {
                "product_id": prod_map["Ігровий монітор ASUS TUF Gaming VG27AQ"],
                "name": "Ігровий монітор ASUS TUF Gaming VG27AQ",
                "quantity": 1,
                "unit_price": 13999.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-107",
        "customer_id": cust_map["CUST-001"],
        "order_date": datetime.datetime(2026, 3, 18, 17, 10),
        "status": "processing",
        "payment_method": "card",
        "total_amount": 7899.0,
        "items": [
            {
                "product_id": prod_map["SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe"],
                "name": "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe",
                "quantity": 1,
                "unit_price": 7899.0
            }
        ]
    },
    {
        "order_number": "ORD-2026-108",
        "customer_id": cust_map["CUST-008"],
        "order_date": datetime.datetime(2026, 3, 19, 13, 0),
        "status": "shipped",
        "payment_method": "card",
        "total_amount": 5499.0,
        "items": [
            {
                "product_id": prod_map["Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000"],
                "name": "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000",
                "quantity": 1,
                "unit_price": 5499.0
            }
        ]
    }
]

res_ord = db.orders.insert_many(orders_data)

# виводимо кількість завантажених сутностей
print(f"Products count: {db.products.count_documents({})}")
print(f"Customers count: {db.customers.count_documents({})}")
print(f"Orders count: {db.orders.count_documents({})}")

# 1. демонстрація базових crud операцій
# вставка одиничного документа
new_prod = {
    "name": "Термопаста Arctic MX-4 4g",
    "category": "Охолодження",
    "price": 299.0,
    "in_stock": True,
    "stock_quantity": 50,
    "tags": ["thermal-paste", "arctic", "cooling"]
}
insert_res = db.products.insert_one(new_prod)
print(f"Inserted single product id: {insert_res.inserted_id}")

# оновлення документа
db.products.update_one(
    {"_id": insert_res.inserted_id},
    {"$set": {"price": 279.0, "promo": True}}
)

# перевірка оновлення
updated_doc = db.products.find_one({"_id": insert_res.inserted_id})
print(f"Updated product price: {updated_doc['price']}, promo: {updated_doc.get('promo')}")

# вилучення одиничного документа
del_res = db.products.delete_one({"_id": insert_res.inserted_id})
print(f"Deleted temporary products: {del_res.deleted_count}")

# 2. демонстрація пошуку за вкладеними полями (embedded documents)
print("\n--- Products with AM5 socket (Embedded Document Query) ---")
am5_query = db.products.find(
    {"specifications.socket": "AM5"},
    {"name": 1, "price": 1, "specifications.socket": 1, "_id": 0}
)
for p in am5_query:
    print(f"- {p['name']}: {p['price']} UAH, socket: {p['specifications']['socket']}")

print("\n--- Customers living in Lviv (Embedded Address Query) ---")
lviv_query = db.customers.find(
    {"address.city": "Львів"},
    {"name": 1, "phone": 1, "address.street": 1, "_id": 0}
)
for c in lviv_query:
    print(f"- {c['name']} ({c['phone']}): {c['address']['street']}")

# 3. демонстрація пошуку за посиланнями (references через objectid)
print("\n--- Orders for customer CUST-001 via ObjectId reference ---")
cust1_id = cust_map["CUST-001"]
cust1_orders = db.orders.find({"customer_id": cust1_id})
for o in cust1_orders:
    print(f"- Order {o['order_number']}: {o['total_amount']} UAH, status: {o['status']}")

# 4. демонстрація агрегації $lookup (з'єднання orders та customers)
print("\n--- Aggregation $lookup: Orders joined with Customers ---")
lookup_pipeline = [
    {"$match": {"status": "completed"}},
    {
        "$lookup": {
            "from": "customers",
            "localField": "customer_id",
            "foreignField": "_id",
            "as": "customer_info"
        }
    },
    {"$unwind": "$customer_info"},
    {
        "$project": {
            "_id": 0,
            "order_number": 1,
            "total_amount": 1,
            "customer_name": "$customer_info.name",
            "customer_city": "$customer_info.address.city",
            "customer_email": "$customer_info.email"
        }
    }
]

lookup_results = list(db.orders.aggregate(lookup_pipeline))
for r in lookup_results:
    print(f"- {r['order_number']}: {r['total_amount']} UAH | Customer: {r['customer_name']} ({r['customer_city']})")
