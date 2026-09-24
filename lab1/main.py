import time
import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# 1. порівняння схем та бенчмарк: реляційна модель (sql) vs документна (nosql)
# -------------------------------------------------------------
def benchmark_sql_vs_nosql():
    print("=== 1. Тестування продуктивності: SQL (SQLite) vs NoSQL (Document Store) ===")

    # ініціалізуємо sqlite в оперативній пам'яті
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # створюємо нормалізовані таблиці з foreign keys
    cur.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )""")
    cur.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        order_date TEXT,
        total_amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")
    cur.execute("""
    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )""")
    conn.commit()

    # документне сховище (in-memory колекція документів)
    nosql_doc_store = {}

    n_records = 3000

    # бенчмарк вставки в sql (потрібно вставити юзера, замовлення та позиції)
    t0_sql_insert = time.perf_counter()
    for i in range(1, n_records + 1):
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (i, f"Користувач {i}", f"user{i}@lnu.edu.ua"))
        cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (i, i, "2026-09-24", 1500.0 + i))
        cur.execute("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
                    (i * 2 - 1, i, "Ноутбук ThinkPad", "Electronics", 1200.0, 1))
        cur.execute("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
                    (i * 2, i, "Бездротова мишка", "Accessories", 300.0 + i, 1))
    conn.commit()
    t_sql_insert = time.perf_counter() - t0_sql_insert

    # бенчмарк вставки в nosql (один вкладений агрегатний документ)
    t0_nosql_insert = time.perf_counter()
    for i in range(1, n_records + 1):
        # документо-орієнтований підхід: гетерогенні атрибути без фіксованої схеми
        doc = {
            "_id": i,
            "user": {"name": f"Користувач {i}", "email": f"user{i}@lnu.edu.ua"},
            "order_date": "2026-09-24",
            "total_amount": 1500.0 + i,
            "items": [
                {
                    "product_name": "Ноутбук ThinkPad",
                    "category": "Electronics",
                    "price": 1200.0,
                    "quantity": 1,
                    "specs": {"cpu": "Core Ultra 7", "ram_gb": 32, "screen": 14.0}
                },
                {
                    "product_name": "Бездротова мишка",
                    "category": "Accessories",
                    "price": 300.0 + i,
                    "quantity": 1,
                    "specs": {"wireless": True, "dpi": 4000}
                }
            ]
        }
        nosql_doc_store[i] = doc
    t_nosql_insert = time.perf_counter() - t0_nosql_insert

    # бенчмарк вибірки з sql через join трьох таблиць
    t0_sql_query = time.perf_counter()
    for i in range(1, n_records + 1):
        cur.execute("""
            SELECT u.name, u.email, o.order_date, o.total_amount, oi.product_name, oi.price, oi.quantity
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_id = ?
        """, (i,))
        rows = cur.fetchall()
    t_sql_query = time.perf_counter() - t0_sql_query

    # бенчмарк вибірки з nosql (прямий пошук за ключем документа без join)
    t0_nosql_query = time.perf_counter()
    for i in range(1, n_records + 1):
        doc = nosql_doc_store[i]
        _ = doc["user"]["name"], doc["items"]
    t_nosql_query = time.perf_counter() - t0_nosql_query

    conn.close()

    print(f"Кількість записів: {n_records}")
    print(f"SQL вставка (3 таблиці + foreign keys): {t_sql_insert:.4f} с")
    print(f"NoSQL вставка (вкладені документи):      {t_nosql_insert:.4f} с (прискорення: {t_sql_insert / t_nosql_insert:.1f}x)")
    print(f"SQL вибірка (3-way JOIN):               {t_sql_query:.4f} с")
    print(f"NoSQL вибірка (пряме читання за ID):    {t_nosql_query:.4f} с (прискорення: {t_sql_query / t_nosql_query:.1f}x)\n")

    return {
        "sql_insert": t_sql_insert,
        "nosql_insert": t_nosql_insert,
        "sql_query": t_sql_query,
        "nosql_query": t_nosql_query
    }

# -------------------------------------------------------------
# 2. емуляція теореми cap: поведінка cp (банк) vs ap (youtube) при розриві зв'язку
# -------------------------------------------------------------
class DistributedClusterNode:
    def __init__(self, node_id, mode="CP"):
        self.node_id = node_id
        self.mode = mode  # CP або AP
        self.data_store = {}
        self.pending_sync_queue = []
        self.peer_node = None
        self.network_partitioned = False

    def link_peer(self, peer):
        self.peer_node = peer

    def set_partition(self, is_partitioned):
        self.network_partitioned = is_partitioned

    def execute_write(self, key, value):
        # сценарій cp (банківський переказ): строга узгодженість
        if self.mode == "CP":
            if self.network_partitioned:
                # при розриві мережі вузол блокує запис щоб не допустити неузгодженості
                return False, f"[{self.node_id} - CP MODE] ВІДХИЛЕНО: Мережеве розщеплення (Partition). Запис заблоковано для збереження цілісності балансу."
            else:
                self.data_store[key] = value
                if self.peer_node and not self.network_partitioned:
                    self.peer_node.data_store[key] = value
                return True, f"[{self.node_id} - CP MODE] УСПІХ: Баланс оновлено синхронно на всіх репліках."

        # сценарій ap (youtube коментар / лайк): висока доступність
        elif self.mode == "AP":
            self.data_store[key] = value
            if self.network_partitioned:
                # приймаємо запис локально та ставимо в чергу асинхронної реплікації
                self.pending_sync_queue.append((key, value))
                return True, f"[{self.node_id} - AP MODE] УСПІХ (Eventual): Коментар збережено локально. Поставлено в чергу на реплікацію."
            else:
                if self.peer_node:
                    self.peer_node.data_store[key] = value
                return True, f"[{self.node_id} - AP MODE] УСПІХ: Коментар збережено та репліковано."

    def heal_network(self):
        self.network_partitioned = False
        # синхронізація черги після відновлення зв'язку
        synced_count = len(self.pending_sync_queue)
        while self.pending_sync_queue:
            k, v = self.pending_sync_queue.pop(0)
            if self.peer_node:
                self.peer_node.data_store[k] = v
        return synced_count

def demo_cap_simulation():
    print("=== 2. Емуляція CAP-теореми: CP (Банк) vs AP (YouTube коментарі) ===")

    # 1. CP вузли банку
    bank_node_a = DistributedClusterNode("Вузол_A (Київ)", mode="CP")
    bank_node_b = DistributedClusterNode("Вузол_B (Львів)", mode="CP")
    bank_node_a.link_peer(bank_node_b)
    bank_node_b.link_peer(bank_node_a)

    print("--- Сценарій 1: Банківська транзакція (CP система) ---")
    status, msg = bank_node_a.execute_write("рахунок_1001", 50000.0)
    print(f"Звичайний режим: {msg}")

    # виникає розрив мережі між києвом та львовом
    bank_node_a.set_partition(True)
    bank_node_b.set_partition(True)
    print("[МЕРЕЖЕВИЙ ЗБІЙ] Канал між Вузлом_A та Вузлом_B розірвано.")

    status, msg = bank_node_a.execute_write("рахунок_1001", 35000.0)
    print(f"Спроба списання при розриві: {msg}")

    # 2. AP вузли соціальної мережі
    yt_node_a = DistributedClusterNode("Edge_Вузол_A", mode="AP")
    yt_node_b = DistributedClusterNode("Edge_Вузол_B", mode="AP")
    yt_node_a.link_peer(yt_node_b)
    yt_node_b.link_peer(yt_node_a)

    print("\n--- Сценарій 2: Коментар на YouTube (AP система) ---")
    yt_node_a.set_partition(True)
    yt_node_b.set_partition(True)
    print("[МЕРЕЖЕВИЙ ЗБІЙ] Канал між регіональними вузлами розірвано.")

    status, msg = yt_node_a.execute_write("video_99_comment", "Чудова лекція про NoSQL!")
    print(f"Публікація при розриві: {msg}")
    print(f"Стан вузла B до синхронізації: {yt_node_b.data_store.get('video_99_comment', 'Коментар ще не надійшов')}")

    # відновлюємо зв'язок
    synced = yt_node_a.heal_network()
    print(f"[МЕРЕЖУ ВІДНОВЛЕНО] Синхронізовано {synced} відкладених операцій.")
    print(f"Стан вузла B після синхронізації: {yt_node_b.data_store.get('video_99_comment')}\n")

# -------------------------------------------------------------
# 3. демонстрація polyglot persistence (redis + mongodb + sql)
# -------------------------------------------------------------
def demo_polyglot_persistence():
    print("=== 3. Демонстрація архітектури Polyglot Persistence ===")

    # 1. key-value (redis) для кешування сесій та швидкого лічильника
    redis_cache = {
        "session:user_77": {"ip": "194.44.112.5", "token": "jwt_abc123", "ttl_sec": 3600},
        "rate_limit:user_77:requests_per_min": 14
    }

    # 2. document store (mongodb) для гнучкого каталогу товарів з різними полями
    mongo_catalog = [
        {
            "_id": "prod_1",
            "title": "Ноутбук",
            "category": "Computers",
            "attributes": {"cpu": "M3 Max", "ram": 36, "display": "Liquid Retina"}
        },
        {
            "_id": "prod_2",
            "title": "Книга 'NoSQL Distilled'",
            "category": "Books",
            "attributes": {"author": "Martin Fowler", "pages": 192, "isbn": "978-0321826626"}
        }
    ]

    # 3. relational database (postgresql/mysql) для транзакцій оплати
    sql_ledger = [
        {"tx_id": "TX_9001", "user_id": 77, "amount": 2400.0, "status": "SETTLED", "timestamp": "2026-09-24 14:30:00"}
    ]

    print("1. In-Memory Key-Value (Redis): Кеш авторизації та лічильники запитів")
    print(f"   Сесія: {redis_cache['session:user_77']}")
    print("2. Document Store (MongoDB): Каталог товарів із динамічною поліморфною структурою")
    for p in mongo_catalog:
        print(f"   Товар: {p['title']} ({p['category']}) -> атрибути: {p['attributes']}")
    print("3. Relational ACID DB (PostgreSQL): Фінансовий журнал платежів")
    print(f"   Проводка: {sql_ledger[0]}\n")

# -------------------------------------------------------------
# 4. візуалізація трендів db-engines ranking та характеристик
# -------------------------------------------------------------
def plot_db_trends(bench_data):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    # 1. графік порівняння швидкості sql vs nosql
    ax1 = axes[0, 0]
    categories = ["Вставка (Insert)", "Вибірка (Query)"]
    sql_times = [bench_data["sql_insert"] * 1000, bench_data["sql_query"] * 1000]
    nosql_times = [bench_data["nosql_insert"] * 1000, bench_data["nosql_query"] * 1000]

    x = np.arange(len(categories))
    width = 0.35
    ax1.bar(x - width/2, sql_times, width, label="SQL (SQLite JOIN)", color="#4682B4")
    ax1.bar(x + width/2, nosql_times, width, label="NoSQL (Document Store)", color="#2E8B57")
    ax1.set_ylabel("Час виконання (мс)")
    ax1.set_title("Порівняння часу виконання операцій (3000 записів)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 2. графік популярності nosql за даними db-engines ranking (2024-2026)
    ax2 = axes[0, 1]
    years = [2024, 2025, 2026]
    mongodb_scores = [420.5, 415.2, 408.7]
    redis_scores = [155.0, 158.4, 162.1]
    elasticsearch_scores = [135.2, 140.8, 145.0]
    cassandra_scores = [110.4, 105.1, 101.3]
    neo4j_scores = [52.1, 55.6, 58.9]

    ax2.plot(years, mongodb_scores, marker="o", linewidth=2.2, label="MongoDB (Document)", color="#13aa52")
    ax2.plot(years, redis_scores, marker="s", linewidth=2.2, label="Redis (Key-Value)", color="#d82c20")
    ax2.plot(years, elasticsearch_scores, marker="^", linewidth=2.2, label="Elasticsearch (Search/Doc)", color="#005571")
    ax2.plot(years, cassandra_scores, marker="d", linewidth=2.2, label="Cassandra (Wide-Column)", color="#1b6388")
    ax2.plot(years, neo4j_scores, marker="v", linewidth=2.2, label="Neo4j (Graph)", color="#018bff")

    ax2.set_title("Тренди популярності NoSQL СУБД (DB-Engines Ranking)")
    ax2.set_xlabel("Рік")
    ax2.set_ylabel("Бали популярності DB-Engines")
    ax2.set_xticks(years)
    ax2.legend(fontsize=8.5)
    ax2.grid(True, linestyle="--", alpha=0.5)

    # 3. порівняння вартості масштабування scale-up vs scale-out
    ax3 = axes[1, 0]
    load_units = np.linspace(1, 10, 100)
    scale_up_cost = 10 * np.exp(0.45 * load_units)
    scale_out_cost = 15 * load_units + 5

    ax3.plot(load_units, scale_up_cost, label="Scale-up (Вертикальне: потужніший сервер)", color="#d9534f", linewidth=2.2)
    ax3.plot(load_units, scale_out_cost, label="Scale-out (Горизонтальне: кластер NoSQL)", color="#5cb85c", linewidth=2.2)
    ax3.set_title("Економіка масштабування: Scale-Up vs Scale-Out")
    ax3.set_xlabel("Навантаження системи (умовні одиниці)")
    ax3.set_ylabel("Вартість інфраструктури ($)")
    ax3.legend(fontsize=8.5)
    ax3.grid(True, linestyle="--", alpha=0.5)

    # 4. структура cap теореми (трикутник компромісів)
    ax4 = axes[1, 1]
    ax4.axis("off")
    cap_text = (
        "ТЕОРЕМА CAP (БРЮЕРА):\n\n"
        "1. Consistency (Узгодженість):\n"
        "   Всі вузли бачать однакові дані в один момент часу.\n\n"
        "2. Availability (Доступність):\n"
        "   Кожен запит отримує відповідь (без гарантії найновіших даних).\n\n"
        "3. Partition Tolerance (Стійкість до розриву):\n"
        "   Система працює при збоях зв'язку між серверами.\n\n"
        "ГОЛОВНИЙ ВИСНОВОК:\n"
        "У розподіленій мережі збої (P) є неминучими.\n"
        "Тому реальний вибір завжди стоїть між:\n"
        "-> CP: Банківські операції, білінг (Consistency > Availability)\n"
        "-> AP: Стрічки соцмереж, коментарі (Availability > Consistency)"
    )
    ax4.text(0.05, 0.95, cap_text, transform=ax4.transAxes, fontsize=9.5,
             verticalalignment="top", fontfamily="sans-serif",
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f8f9fa", edgecolor="#ced4da"))

    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# головна точка входу
# -------------------------------------------------------------
if __name__ == "__main__":
    bench_data = benchmark_sql_vs_nosql()
    demo_cap_simulation()
    demo_polyglot_persistence()
    plot_db_trends(bench_data)
