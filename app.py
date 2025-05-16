import falcon
import json
import sqlite3
from math import sqrt

DB_PATH = 'delivery.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_distance(lat1, lon1, lat2, lon2):
    # Simple Euclidean for demo, replace with Haversine for real
    return sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111  # rough km conversion

class WarehouseResource:
    def on_get(self, req, resp):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM warehouses")
        warehouses = [dict(row) for row in cursor.fetchall()]
        resp.media = warehouses
        conn.close()

class AgentResource:
    def on_get(self, req, resp, warehouse_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE warehouse_id = ?", (warehouse_id,))
        agents = [dict(row) for row in cursor.fetchall()]
        resp.media = agents
        conn.close()

class OrdersResource:
    def on_get(self, req, resp, warehouse_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE warehouse_id = ? AND status = 'pending'", (warehouse_id,))
        orders = [dict(row) for row in cursor.fetchall()]
        resp.media = orders
        conn.close()

class AssignOrdersResource:
    def on_post(self, req, resp, warehouse_id):
        """
        Allocation logic:
        - Assign orders to agents respecting max hours & max km
        - Approx 5 mins per km means max 1200 mins driving (100km * 5min)
        - Max 10 hours = 600 mins work - so orders/time must fit
        - Each order: approximate 10 mins + travel
        - Use simple nearest agent assignment (greedy)
        """
        conn = get_db()
        cursor = conn.cursor()

        # Fetch agents and orders
        cursor.execute("SELECT * FROM agents WHERE warehouse_id = ?", (warehouse_id,))
        agents = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT * FROM orders WHERE warehouse_id = ? AND status = 'pending'", (warehouse_id,))
        orders = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT * FROM warehouses WHERE id = ?", (warehouse_id,))
        warehouse = cursor.fetchone()

        if not agents or not orders or not warehouse:
            resp.status = falcon.HTTP_404
            resp.media = {"error": "No agents or orders or warehouse found"}
            conn.close()
            return

        # Reset agents daily_orders before allocation
        for agent in agents:
            cursor.execute("UPDATE agents SET daily_orders = 0 WHERE id = ?", (agent['id'],))
        conn.commit()

        # Initialize agent states
        agent_state = {
            agent['id']: {
                'orders': [],
                'hours': 0,
                'km': 0,
                'lat': warehouse['lat'],
                'lon': warehouse['lon']
            } for agent in agents
        }

        # Assign orders to agents
        for order in orders:
            # Find suitable agent who can take the order
            assigned = False
            for agent_id, state in agent_state.items():
                # Calculate distance from last point to order location
                dist = calculate_distance(state['lat'], state['lon'], order['lat'], order['lon'])
                time_needed = dist * 5 + 10  # 5 mins/km + 10 mins per order delivery

                if (state['hours'] + time_needed / 60) <= 10 and (state['km'] + dist) <= 100:
                    # Assign order
                    state['orders'].append(order['id'])
                    state['hours'] += time_needed / 60
                    state['km'] += dist
                    state['lat'] = order['lat']
                    state['lon'] = order['lon']
                    assigned = True
                    break

            if not assigned:
                # Order postponed - skip assigning
                continue

        # Update DB with assignments
        total_assigned = 0
        for agent_id, state in agent_state.items():
            order_ids = state['orders']
            cursor.execute("UPDATE agents SET daily_orders = ? WHERE id = ?", (len(order_ids), agent_id))
            for oid in order_ids:
                cursor.execute("UPDATE orders SET assigned_agent_id = ?, status = 'assigned' WHERE id = ?", (agent_id, oid))
            total_assigned += len(order_ids)
        conn.commit()

        resp.media = {
            "message": f"Assigned {total_assigned} orders in warehouse {warehouse_id}",
            "details": agent_state
        }
        conn.close()

class HomeResource:
    def on_get(self, req, resp):
        with open("templates/index.html", "r") as f:
            html = f.read()
        resp.content_type = 'text/html'
        resp.text = html

# Falcon app setup
app = falcon.App()

# Routes
app.add_route('/', HomeResource())
app.add_route('/warehouses', WarehouseResource())
app.add_route('/warehouses/{warehouse_id}/agents', AgentResource())
app.add_route('/warehouses/{warehouse_id}/orders', OrdersResource())
app.add_route('/warehouses/{warehouse_id}/assign', AssignOrdersResource())
