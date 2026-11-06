// лабораторна робота №3: створення та моделювання баз даних в mongodb
// використання бази techstore

// перемикаємось на базу techstore
db = db.getSiblingDB("techstore");

// очищаємо старі дані для чистого запуску
db.products.drop();
db.customers.drop();
db.orders.drop();

// 1. створення колекції товарів (10 документів, 5+ різних типів даних bson)
db.products.insertMany([
  {
    name: "Процесор AMD Ryzen 7 7800X3D",
    category: "Процесори",
    price: 18499.0,
    in_stock: true,
    stock_quantity: 25,
    tags: ["cpu", "am5", "gaming", "v-cache"],
    specifications: {
      socket: "AM5",
      cores: 8,
      threads: 16,
      base_clock_ghz: 4.2,
      tdp_watts: 120,
      ram_type: "DDR5"
    }
  },
  {
    name: "Процесор Intel Core i7-14700K",
    category: "Процесори",
    price: 17299.0,
    in_stock: true,
    stock_quantity: 18,
    tags: ["cpu", "lga1700", "raptor-lake"],
    specifications: {
      socket: "LGA1700",
      cores: 20,
      threads: 28,
      base_clock_ghz: 3.4,
      tdp_watts: 125,
      ram_type: "DDR5"
    }
  },
  {
    name: "Відеокарта ASUS ROG Strix GeForce RTX 4080 Super",
    category: "Відеокарти",
    price: 49999.0,
    in_stock: true,
    stock_quantity: 7,
    tags: ["gpu", "nvidia", "rtx", "4k-gaming"],
    specifications: {
      vram_gb: 16,
      bus_width_bit: 256,
      interface: "PCI-e 4.0",
      recommended_psu_watts: 750
    }
  },
  {
    name: "Відеокарта Sapphire Nitro+ Radeon RX 7900 XTX",
    category: "Відеокарти",
    price: 43500.0,
    in_stock: false,
    stock_quantity: 0,
    tags: ["gpu", "amd", "radeon", "rdna3"],
    specifications: {
      vram_gb: 24,
      bus_width_bit: 384,
      interface: "PCI-e 4.0",
      recommended_psu_watts: 800
    }
  },
  {
    name: "Материнська плата MSI MAG B650 TOMAHAWK WIFI",
    category: "Материнські плати",
    price: 8999.0,
    in_stock: true,
    stock_quantity: 14,
    tags: ["motherboard", "am5", "wifi6e", "atx"],
    specifications: {
      socket: "AM5",
      form_factor: "ATX",
      ram_slots: 4,
      max_ram_gb: 192,
      ram_type: "DDR5"
    }
  },
  {
    name: "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000",
    category: "Оперативна пам'ять",
    price: 5499.0,
    in_stock: true,
    stock_quantity: 30,
    tags: ["ram", "ddr5", "cl32", "rgb"],
    specifications: {
      capacity_gb: 32,
      ram_type: "DDR5",
      frequency_mhz: 6000,
      kit: "2x16GB",
      voltage: 1.35
    }
  },
  {
    name: "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe",
    category: "Накопичувачі",
    price: 7899.0,
    in_stock: true,
    stock_quantity: 22,
    tags: ["ssd", "nvme", "pcie4", "m2"],
    specifications: {
      form_factor: "M.2 2280",
      capacity_gb: 2000,
      read_speed_mb: 7450,
      write_speed_mb: 6900
    }
  },
  {
    name: "Блок живлення Seasonic Focus GX-850 850W Gold",
    category: "Блоки живлення",
    price: 6299.0,
    in_stock: true,
    stock_quantity: 12,
    tags: ["psu", "modular", "80plus-gold"],
    specifications: {
      power_watts: 850,
      efficiency: "80 PLUS Gold",
      modular: "full",
      fan_size_mm: 120
    }
  },
  {
    name: "Корпус Fractal Design North Charcoal Black",
    category: "Корпуси",
    price: 6899.0,
    in_stock: true,
    stock_quantity: 9,
    tags: ["case", "mid-tower", "wood-front", "mesh"],
    specifications: {
      form_factor: "Mid-Tower",
      supported_motherboards: ["ATX", "Micro-ATX", "Mini-ITX"],
      gpu_max_length_mm: 355
    }
  },
  {
    name: "Ігровий монітор ASUS TUF Gaming VG27AQ",
    category: "Монітори",
    price: 13999.0,
    in_stock: true,
    stock_quantity: 15,
    tags: ["monitor", "2k", "ips", "165hz", "g-sync"],
    specifications: {
      diagonal_inch: 27.0,
      resolution: "2560x1440",
      matrix: "IPS",
      refresh_rate_hz: 165
    }
  }
]);

// 2. створення колекції клієнтів (10 документів з вкладеними адресами)
db.customers.insertMany([
  {
    customer_code: "CUST-001",
    name: "Олександр Мельник",
    email: "o.melnyk@gmail.com",
    phone: "+380501112233",
    loyalty_level: "gold",
    discount_pct: 10,
    address: {
      city: "Львів",
      street: "вул. Франка, 15",
      apartment: 4,
      zip: "79005"
    }
  },
  {
    customer_code: "CUST-002",
    name: "Ірина Ковальчук",
    email: "i.koval@ukr.net",
    phone: "+380672223344",
    loyalty_level: "silver",
    discount_pct: 5,
    address: {
      city: "Київ",
      street: "просп. Перемоги, 42",
      apartment: 128,
      zip: "03057"
    }
  },
  {
    customer_code: "CUST-003",
    name: "Максим Шевченко",
    email: "m.sheva@tech.io",
    phone: "+380933334455",
    loyalty_level: "platinum",
    discount_pct: 15,
    address: {
      city: "Львів",
      street: "вул. Городоцька, 110",
      apartment: 22,
      zip: "79018"
    }
  },
  {
    customer_code: "CUST-004",
    name: "Анна Бондаренко",
    email: "a.bond@outlook.com",
    phone: "+380634445566",
    loyalty_level: "standard",
    discount_pct: 0,
    address: {
      city: "Харків",
      street: "вул. Сумська, 5",
      apartment: 18,
      zip: "61057"
    }
  },
  {
    customer_code: "CUST-005",
    name: "Тарас Романюк",
    email: "t.romanyuk@gmail.com",
    phone: "+380975556677",
    loyalty_level: "gold",
    discount_pct: 10,
    address: {
      city: "Івано-Франківськ",
      street: "вул. Незалежності, 73",
      apartment: 9,
      zip: "76018"
    }
  },
  {
    customer_code: "CUST-006",
    name: "Дмитро Сидоренко",
    email: "d.sydor@meta.ua",
    phone: "+380506667788",
    loyalty_level: "silver",
    discount_pct: 5,
    address: {
      city: "Дніпро",
      street: "просп. Яворницького, 18",
      apartment: 55,
      zip: "49000"
    }
  },
  {
    customer_code: "CUST-007",
    name: "Олена Василенко",
    email: "olena.v@yahoo.com",
    phone: "+380677778899",
    loyalty_level: "standard",
    discount_pct: 0,
    address: {
      city: "Львів",
      street: "вул. Стрийська, 85",
      apartment: 64,
      zip: "79031"
    }
  },
  {
    customer_code: "CUST-008",
    name: "Андрій Ткачук",
    email: "a.tkachuk@gmail.com",
    phone: "+380938889900",
    loyalty_level: "gold",
    discount_pct: 10,
    address: {
      city: "Тернопіль",
      street: "вул. Руська, 12",
      apartment: 3,
      zip: "46001"
    }
  },
  {
    customer_code: "CUST-009",
    name: "Вікторія Мороз",
    email: "v.moroz@icloud.com",
    phone: "+380991234567",
    loyalty_level: "platinum",
    discount_pct: 15,
    address: {
      city: "Київ",
      street: "вул. Хрещатик, 24",
      apartment: 30,
      zip: "01001"
    }
  },
  {
    customer_code: "CUST-010",
    name: "Сергій Кравченко",
    email: "s.kravch@ukr.net",
    phone: "+380967654321",
    loyalty_level: "silver",
    discount_pct: 5,
    address: {
      city: "Одеса",
      street: "вул. Дерибасівська, 9",
      apartment: 15,
      zip: "65026"
    }
  }
]);

// отримуємо збережені id клієнтів та товарів для зв'язків
var cust1 = db.customers.findOne({ customer_code: "CUST-001" })._id;
var cust2 = db.customers.findOne({ customer_code: "CUST-002" })._id;
var cust3 = db.customers.findOne({ customer_code: "CUST-003" })._id;
var cust5 = db.customers.findOne({ customer_code: "CUST-005" })._id;
var cust7 = db.customers.findOne({ customer_code: "CUST-007" })._id;
var cust8 = db.customers.findOne({ customer_code: "CUST-008" })._id;
var cust9 = db.customers.findOne({ customer_code: "CUST-009" })._id;

var prodRyzen = db.products.findOne({ name: "Процесор AMD Ryzen 7 7800X3D" })._id;
var prodB650 = db.products.findOne({ name: "Материнська плата MSI MAG B650 TOMAHAWK WIFI" })._id;
var prodRtx = db.products.findOne({ name: "Відеокарта ASUS ROG Strix GeForce RTX 4080 Super" })._id;
var prodRam = db.products.findOne({ name: "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000" })._id;
var prodSsd = db.products.findOne({ name: "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe" })._id;
var prodPsu = db.products.findOne({ name: "Блок живлення Seasonic Focus GX-850 850W Gold" })._id;
var prodCase = db.products.findOne({ name: "Корпус Fractal Design North Charcoal Black" })._id;
var prodMon = db.products.findOne({ name: "Ігровий монітор ASUS TUF Gaming VG27AQ" })._id;
var prodIntel = db.products.findOne({ name: "Процесор Intel Core i7-14700K" })._id;

// 3. створення замовлень (references через objectid та вкладені items)
db.orders.insertMany([
  {
    order_number: "ORD-2026-101",
    customer_id: cust1,
    order_date: new Date("2026-03-10T11:30:00Z"),
    status: "completed",
    payment_method: "card",
    total_amount: 27498.0,
    items: [
      { product_id: prodRyzen, name: "Процесор AMD Ryzen 7 7800X3D", quantity: 1, unit_price: 18499.0 },
      { product_id: prodB650, name: "Материнська плата MSI MAG B650 TOMAHAWK WIFI", quantity: 1, unit_price: 8999.0 }
    ]
  },
  {
    order_number: "ORD-2026-102",
    customer_id: cust3,
    order_date: new Date("2026-03-11T14:15:00Z"),
    status: "completed",
    payment_method: "bank_transfer",
    total_amount: 49999.0,
    items: [
      { product_id: prodRtx, name: "Відеокарта ASUS ROG Strix GeForce RTX 4080 Super", quantity: 1, unit_price: 49999.0 }
    ]
  },
  {
    order_number: "ORD-2026-103",
    customer_id: cust2,
    order_date: new Date("2026-03-12T16:40:00Z"),
    status: "completed",
    payment_method: "card",
    total_amount: 13398.0,
    items: [
      { product_id: prodRam, name: "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000", quantity: 1, unit_price: 5499.0 },
      { product_id: prodSsd, name: "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe", quantity: 1, unit_price: 7899.0 }
    ]
  },
  {
    order_number: "ORD-2026-104",
    customer_id: cust5,
    order_date: new Date("2026-03-14T10:05:00Z"),
    status: "processing",
    payment_method: "cash_on_delivery",
    total_amount: 13198.0,
    items: [
      { product_id: prodPsu, name: "Блок живлення Seasonic Focus GX-850 850W Gold", quantity: 1, unit_price: 6299.0 },
      { product_id: prodCase, name: "Корпус Fractal Design North Charcoal Black", quantity: 1, unit_price: 6899.0 }
    ]
  },
  {
    order_number: "ORD-2026-105",
    customer_id: cust7,
    order_date: new Date("2026-03-15T12:50:00Z"),
    status: "shipped",
    payment_method: "card",
    total_amount: 13999.0,
    items: [
      { product_id: prodMon, name: "Ігровий монітор ASUS TUF Gaming VG27AQ", quantity: 1, unit_price: 13999.0 }
    ]
  },
  {
    order_number: "ORD-2026-106",
    customer_id: cust9,
    order_date: new Date("2026-03-16T09:20:00Z"),
    status: "completed",
    payment_method: "bank_transfer",
    total_amount: 31298.0,
    items: [
      { product_id: prodIntel, name: "Процесор Intel Core i7-14700K", quantity: 1, unit_price: 17299.0 },
      { product_id: prodMon, name: "Ігровий монітор ASUS TUF Gaming VG27AQ", quantity: 1, unit_price: 13999.0 }
    ]
  },
  {
    order_number: "ORD-2026-107",
    customer_id: cust1,
    order_date: new Date("2026-03-18T17:10:00Z"),
    status: "processing",
    payment_method: "card",
    total_amount: 7899.0,
    items: [
      { product_id: prodSsd, name: "SSD накопичувач Samsung 990 Pro 2TB M.2 NVMe", quantity: 1, unit_price: 7899.0 }
    ]
  },
  {
    order_number: "ORD-2026-108",
    customer_id: cust8,
    order_date: new Date("2026-03-19T13:00:00Z"),
    status: "shipped",
    payment_method: "card",
    total_amount: 5499.0,
    items: [
      { product_id: prodRam, name: "Оперативна пам'ять Kingston Fury Renegade 32GB DDR5-6000", quantity: 1, unit_price: 5499.0 }
    ]
  }
]);

print("Наповнення завершено:");
print("Товарів у базі:", db.products.countDocuments());
print("Клієнтів у базі:", db.customers.countDocuments());
print("Замовлень у базі:", db.orders.countDocuments());

// 4. демонстрація базових crud операцій
print("\n--- Демонстрація CRUD операцій ---");

// вставка одиничного документа
db.products.insertOne({
  name: "Клавіатура Keychron Q1 Pro",
  category: "Периферія",
  price: 8200.0,
  in_stock: true,
  stock_quantity: 10,
  tags: ["wireless", "mechanical", "custom"]
});
print("Вставлено одиничний товар: Keychron Q1 Pro");

// пошук товару
var foundProd = db.products.findOne({ category: "Периферія" }, { name: 1, price: 1, _id: 0 });
print("Знайдено в категорії Периферія:", JSON.stringify(foundProd));

// оновлення товару
db.products.updateOne(
  { name: "Клавіатура Keychron Q1 Pro" },
  { $set: { price: 7999.0, promo: true } }
);
print("Оновлено ціну до 7999 грн та додано прапорець promo");

// видалення тимчасового товару
db.products.deleteOne({ name: "Клавіатура Keychron Q1 Pro" });
print("Вилучено тимчасовий товар Keychron Q1 Pro");

// 5. моделювання зв'язків: вкладені документи (embedded documents)
print("\n--- Моделювання: Embedded Documents ---");
print("Процесори з сокетом AM5:");
db.products.find(
  { "specifications.socket": "AM5" },
  { name: 1, price: 1, "specifications.socket": 1, _id: 0 }
).forEach(function(p) {
  print("- " + p.name + " (" + p.price + " грн, сокет: " + p.specifications.socket + ")");
});

print("Клієнти з міста Львів:");
db.customers.find(
  { "address.city": "Львів" },
  { name: 1, phone: 1, "address.street": 1, _id: 0 }
).forEach(function(c) {
  print("- " + c.name + " (" + c.phone + "): " + c.address.street);
});

// 6. моделювання зв'язків: посилання (references через objectid)
print("\n--- Моделювання: References (ObjectId) ---");
print("Замовлення клієнта CUST-001 за ObjectId:");
db.orders.find(
  { customer_id: cust1 },
  { order_number: 1, total_amount: 1, status: 1, _id: 0 }
).forEach(function(o) {
  print("- " + o.order_number + ": " + o.total_amount + " грн [статус: " + o.status + "]");
});

// 7. моделювання зв'язків: агрегація-з'єднання ($lookup)
print("\n--- Моделювання: $lookup агрегація ---");
var lookupRes = db.orders.aggregate([
  { $match: { status: "completed" } },
  {
    $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "_id",
      as: "customer_details"
    }
  },
  { $unwind: "$customer_details" },
  {
    $project: {
      _id: 0,
      order_number: 1,
      total_amount: 1,
      customer_name: "$customer_details.name",
      customer_city: "$customer_details.address.city"
    }
  }
]).toArray();

lookupRes.forEach(function(res) {
  print("- " + res.order_number + ": " + res.total_amount + " грн | Покупець: " + res.customer_name + " (" + res.customer_city + ")");
});
