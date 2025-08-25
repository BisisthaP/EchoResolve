
# import sqlite3
# from random import choice, randint
# from datetime import datetime, timedelta


# # Connect to a new SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect("sample_orders.db")
# cursor = conn.cursor()

# import sqlite3


# # Create the customers table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS customers (
#     customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT,
#     phone TEXT,
#     address TEXT
# )
# ''')

# # Create the orders table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS orders (
#     order_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     customer_id INTEGER,
#     order_date TEXT,
#     delivery_address TEXT,
#     status TEXT,
#     fulfillment_stage TEXT,
#     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
# )
# ''')

# # Commit changes and close the connection
# conn.commit()

# print("Database 'sample_orders.db' with tables 'customers' and 'orders' created successfully.")

# # Sample customer data
# customers = [
#     ("Alice Johnson", "alice@example.com", "123-456-7890", "123 Maple St"),
#     ("Bob Smith", "bob@example.com", "234-567-8901", "456 Oak St"),
#     ("Carol White", "carol@example.com", "345-678-9012", "789 Pine St"),
#     ("David Brown", "david@example.com", "456-789-0123", "321 Birch St"),
#     ("Eva Green", "eva@example.com", "567-890-1234", "654 Cedar St")
# ]

# # Insert customers into the database
# cursor.executemany('''
# INSERT INTO customers (name, email, phone, address)
# VALUES (?, ?, ?, ?)
# ''', customers)

# # Retrieve customer IDs
# cursor.execute("SELECT customer_id FROM customers")
# customer_ids = [row[0] for row in cursor.fetchall()]

# # Sample order statuses and fulfillment stages
# statuses = ["Pending", "Shipped", "Cancelled"]
# fulfillment_stages = ["Processing", "Packed", "Out for Delivery"]

# # Generate and insert orders
# for customer_id in customer_ids:
#     for _ in range(randint(8, 9)):
#         order_date = (datetime.now() - timedelta(days=randint(1, 30))).strftime("%Y-%m-%d")
#         delivery_address = f"{randint(100, 999)} Delivery Ln"
#         status = choice(statuses)
#         fulfillment_stage = choice(fulfillment_stages)
#         cursor.execute('''
#         INSERT INTO orders (customer_id, order_date, delivery_address, status, fulfillment_stage)
#         VALUES (?, ?, ?, ?, ?)
#         ''', (customer_id, order_date, delivery_address, status, fulfillment_stage))

# # Commit changes and close connection
# conn.commit()
# conn.close()

# print("Inserted 5 customers and 8-9 orders per customer into the database.")

import sqlite3

# Connect to the database
conn = sqlite3.connect("sample_orders.db")
cursor = conn.cursor()

# Query all data from customers table
cursor.execute("SELECT * FROM customers")
customers_data = cursor.fetchall()

# Query all data from orders table
cursor.execute("SELECT * FROM orders")
orders_data = cursor.fetchall()

# Close the connection
conn.close()

# Display the results
print("Customers Table:")
for row in customers_data:
    print(row)

print("\nOrders Table:")
for row in orders_data:
    print(row)