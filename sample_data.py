import sqlite3
import random

conn = sqlite3.connect('delivery.db')
c = conn.cursor()

# Insert 10 warehouses (random lat/lon near city center, example)
warehouses = [(f'Warehouse {i+1}', 28.6 + random.uniform(-0.05, 0.05), 77.2 + random.uniform(-0.05, 0.05)) for i in range(10)]
c.executemany('INSERT INTO warehouses (name, lat, lon) VALUES (?, ?, ?)', warehouses)

# Fetch warehouse IDs
c.execute('SELECT id FROM warehouses')
warehouse_ids = [row[0] for row in c.fetchall()]

# Insert 20 agents per warehouse
agents = []
for w_id in warehouse_ids:
    for i in range(20):
        agents.append((f'Agent {w_id}-{i+1}', w_id))
c.executemany('INSERT INTO agents (name, warehouse_id) VALUES (?, ?)', agents)

# Insert 60 orders per agent (so 20*60 = 1200 orders per warehouse)
orders = []
for w_id in warehouse_ids:
    for _ in range(20 * 60):
        lat = 28.6 + random.uniform(-0.05, 0.05)
        lon = 77.2 + random.uniform(-0.05, 0.05)
        orders.append((w_id, 'Random Address', lat, lon))
c.executemany('INSERT INTO orders (warehouse_id, address, lat, lon) VALUES (?, ?, ?, ?)', orders)

conn.commit()
conn.close()
print("Sample data inserted successfully.")
