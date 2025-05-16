import sqlite3

conn = sqlite3.connect('delivery.db')
c = conn.cursor()

# Agents table
c.execute('''
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    warehouse_id INTEGER,
    max_hours INTEGER DEFAULT 10,
    max_km INTEGER DEFAULT 100,
    daily_orders INTEGER DEFAULT 0
)
''')

# Orders table
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER,
    address TEXT,
    lat REAL,
    lon REAL,
    assigned_agent_id INTEGER,
    status TEXT DEFAULT 'pending'  -- pending, assigned, delivered
)
''')

# Warehouses table
c.execute('''
CREATE TABLE IF NOT EXISTS warehouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    lat REAL,
    lon REAL
)
''')

conn.commit()
conn.close()
print("Database and tables created successfully.")
