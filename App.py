# # # import os
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # AGENT_ID = os.getenv("AGENT_ID")
# # # API_KEY = os.getenv("API_KEY")

# # # from elevenlabs.client import ElevenLabs
# # # from elevenlabs.conversational_ai.conversation import Conversation
# # # from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# # # from elevenlabs.types import ConversationConfig

# # # user_name = "Alex"
# # # schedule = "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00"
# # # prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
# # # first_message = f"Hello {user_name}, how can I help you today?"

# # # conversation_override = {
# # #     "agent": {
# # #         "prompt": {
# # #             "prompt": prompt,
# # #         },
# # #         "first_message": first_message,
# # #     },
# # # }

# # # config = ConversationConfig(
# # #     conversation_config_override=conversation_override,
# # #     extra_body={},
# # #     dynamic_variables={},
# # # )

# # # client = ElevenLabs(api_key=API_KEY)
# # # conversation = Conversation(
# # #     client,
# # #     AGENT_ID,
# # #     config=config,
# # #     requires_auth=True,
# # #     audio_interface=DefaultAudioInterface(),
# # # )


# # # def print_agent_response(response):
# # #     print(f"Agent: {response}")


# # # def print_interrupted_response(original, corrected):
# # #     print(f"Agent interrupted, truncated response: {corrected}")


# # # def print_user_transcript(transcript):
# # #     print(f"User: {transcript}")


# # # conversation = Conversation(
# # #     client,
# # #     AGENT_ID,
# # #     config=config,
# # #     requires_auth=True,
# # #     audio_interface=DefaultAudioInterface(),
# # #     callback_agent_response=print_agent_response,
# # #     callback_agent_response_correction=print_interrupted_response,
# # #     callback_user_transcript=print_user_transcript,
# # # )

# # # conversation.start_session()

# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # AGENT_ID = os.getenv("AGENT_ID")
# # API_KEY = os.getenv("API_KEY")

# # from elevenlabs.client import ElevenLabs
# # from elevenlabs.conversational_ai.conversation import Conversation
# # from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# # from elevenlabs.types import ConversationConfig

# # # This list will store the conversation transcript
# # conversation_history = []

# # user_name = "Alex"
# # schedule = "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00"
# # prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
# # first_message = f"Hello {user_name}, how can I help you today?"

# # conversation_override = {
# #     "agent": {
# #         "prompt": {
# #             "prompt": prompt,
# #         },
# #         "first_message": first_message,
# #     },
# # }

# # config = ConversationConfig(
# #     conversation_config_override=conversation_override,
# #     extra_body={},
# #     dynamic_variables={},
# # )

# # client = ElevenLabs(api_key=API_KEY)

# # def on_agent_response(response):
# #     """Callback function to handle and store the agent's response."""
# #     print(f"Agent: {response}")
# #     conversation_history.append(f"Agent: {response}")

# # def on_interrupted_response(original, corrected):
# #     """Callback function to handle interrupted agent responses."""
# #     print(f"Agent interrupted, truncated response: {original}")
# #     # You might want to decide how to log interruptions
# #     conversation_history.append(f"Agent (interrupted): {original}")


# # def on_user_transcript(transcript):
# #     """Callback function to handle and store the user's transcript."""
# #     print(f"User: {transcript}")
# #     conversation_history.append(f"User: {transcript}")


# # conversation = Conversation(
# #     client,
# #     AGENT_ID,
# #     config=config,
# #     requires_auth=True,
# #     audio_interface=DefaultAudioInterface(),
# #     callback_agent_response=on_agent_response,
# #     callback_agent_response_correction=on_interrupted_response,
# #     callback_user_transcript=on_user_transcript,
# # )

# # try:
# #     conversation.start_session()
# #     # The conversation will run here until it's ended by the user
# #     # or another condition.

# # except KeyboardInterrupt:
# #     print("\nConversation ended by user.")

# # finally:
# #     # You can now access the full transcript
# #     print("\n--- Full Conversation Transcript ---")
# #     for line in conversation_history:
# #         print(line)
# import os
# import sqlite3
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs
# from elevenlabs.conversational_ai.conversation import Conversation, ToolCall
# from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# from elevenlabs.types import ConversationConfig

# # --- Configuration and Setup ---
# load_dotenv()
# AGENT_ID = os.getenv("AGENT_ID")
# API_KEY = os.getenv("API_KEY")
# DB_FILE = "sample_orders.db"
# conversation_history = []

# # --- 1. Database Functions (The "Tools") ---
# # These functions contain the actual business logic and interact with the database.

# def db_connect():
#     """Establishes a connection to the SQLite database."""
#     return sqlite3.connect(DB_FILE)

# def get_order_status(order_id: str) -> str:
#     """Fetches the status of a specific order from the database."""
#     print(f"DATABASE: Checking status for order_id: {order_id}")
#     try:
#         conn = db_connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
#         result = cursor.fetchone()
#         conn.close()
#         if result:
#             status, fulfillment = result
#             return f"Success: Order {order_id} has a status of '{status}' and its fulfillment status is '{fulfillment}'."
#         else:
#             return f"Error: Order with ID '{order_id}' was not found."
#     except Exception as e:
#         return f"Error: A database error occurred: {e}"

# def cancel_order(order_id: str) -> str:
#     """Attempts to cancel an order if it has not yet been shipped."""
#     print(f"DATABASE: Attempting to cancel order_id: {order_id}")
#     try:
#         conn = db_connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
#         result = cursor.fetchone()

#         if not result:
#             conn.close()
#             return f"Error: Order with ID '{order_id}' was not found."

#         status, fulfillment = result
#         # Business Rule: Cannot cancel if it's shipped, out for delivery, or already cancelled.
#         if status in ['Shipped', 'Cancelled'] or fulfillment == 'Out for Delivery':
#             conn.close()
#             return f"Error: Cannot cancel order {order_id}. Its status is '{status}' and fulfillment is '{fulfillment}', which is past the cancellation window."

#         cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE order_id = ?", (order_id,))
#         conn.commit()
#         conn.close()
#         return f"Success: Order {order_id} has been successfully cancelled."
#     except Exception as e:
#         return f"Error: A database error occurred: {e}"

# def update_delivery_address(order_id: str, new_address: str) -> str:
#     """Updates the delivery address for an order if it has not been dispatched."""
#     print(f"DATABASE: Attempting to update address for order_id: {order_id}")
#     try:
#         conn = db_connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
#         result = cursor.fetchone()

#         if not result:
#             conn.close()
#             return f"Error: Order with ID '{order_id}' was not found."

#         status, fulfillment = result
#         # Business Rule: Cannot change address if it's already on its way or shipped.
#         if status in ['Shipped', 'Cancelled'] or fulfillment == 'Out for Delivery':
#             conn.close()
#             return f"Error: Cannot update address for order {order_id}. Its fulfillment status is '{fulfillment}', which is too late to change."

#         cursor.execute("UPDATE orders SET shipping_address = ? WHERE order_id = ?", (new_address, order_id))
#         conn.commit()
#         conn.close()
#         return f"Success: The delivery address for order {order_id} has been updated to '{new_address}'."
#     except Exception as e:
#         return f"Error: A database error occurred: {e}"

# def initiate_order_return(order_id: str) -> str:
#     """Initiates a return for an order if it has already been delivered or shipped."""
#     print(f"DATABASE: Attempting to initiate return for order_id: {order_id}")
#     try:
#         conn = db_connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
#         result = cursor.fetchone()

#         if not result:
#             conn.close()
#             return f"Error: Order with ID '{order_id}' was not found."

#         status = result 
#         # Business Rule: Can only return an item that has been shipped.
#         if status not in ['Shipped']:
#              return f"Error: Cannot initiate a return for order {order_id}. The order status is '{status}'. Returns are only possible for shipped items."

#         cursor.execute("UPDATE orders SET status = 'Return Initiated' WHERE order_id = ?", (order_id,))
#         conn.commit()
#         conn.close()
#         return f"Success: A return has been initiated for order {order_id}. Please check your email for instructions on how to proceed."
#     except Exception as e:
#         return f"Error: A database error occurred: {e}"

# # --- 2. Tool Definitions ---
# # This structure describes our Python functions to the AI.
# # The 'description' is crucial for the AI to decide which tool to use.
# tool_definitions = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_order_status",
#             "description": "Use this tool to get the current status and fulfillment details of a customer's order. Ask for the order ID if the user does not provide it.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"type": "string", "description": "The unique identifier for the order, e.g., '10'."},
#                 },
#                 "required": ["order_id"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "cancel_order",
#             "description": "Use this tool to cancel a customer's order. It will only work if the order has not yet been shipped. Always confirm the order ID with the user before using this tool.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"type": "string", "description": "The unique identifier for the order to be cancelled, e.g., '10'."},
#                 },
#                 "required": ["order_id"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "update_delivery_address",
#             "description": "Use this tool to change the shipping address for an order. This is only possible before the order is dispatched. You must get both the order ID and the new, complete address from the user.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"type": "string", "description": "The unique identifier for the order."},
#                     "new_address": {"type": "string", "description": "The full new shipping address."},
#                 },
#                 "required": ["order_id", "new_address"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "initiate_order_return",
#             "description": "Use this tool to start the return process for an order that has already been shipped. Inform the user that they will receive further instructions via email.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"type": "string", "description": "The unique identifier for the order to be returned."},
#                 },
#                 "required": ["order_id"],
#             },
#         },
#     }
# ]

# # A mapping from the function name (string) to the actual Python function object.
# tool_map = {
#     "get_order_status": get_order_status,
#     "cancel_order": cancel_order,
#     "update_delivery_address": update_delivery_address,
#     "initiate_order_return": initiate_order_return,
# }

# # --- 3. Conversational AI Configuration & Callbacks ---

# # NEW: Updated Prompt and First Message
# user_name = "Alex"
# prompt = (
#     "You are a friendly and highly capable customer service assistant. "
#     "Your primary role is to help users manage their orders using the provided tools. "
#     "Always be polite and clear. If you need information like an order ID, ask for it clearly. "
#     "When an action is successful or fails, clearly state the outcome to the user based on the tool's response."
# )
# first_message = f"Hello {user_name}, how can I help you today? You can ask about your schedule or manage a recent order."

# # NEW: Add the tool definitions to the conversation configuration
# conversation_override = {
#     "agent": {
#         "prompt": {"prompt": prompt},
#         "first_message": first_message,
#         "tools": tool_definitions,
#     },
# }

# config = ConversationConfig(
#     conversation_config_override=conversation_override,
# )

# client = ElevenLabs(api_key=API_KEY)

# # Transcript callbacks (unchanged)
# def on_agent_response(response):
#     print(f"Agent: {response}")
#     conversation_history.append(f"Agent: {response}")

# def on_interrupted_response(original, corrected):
#     print(f"Agent interrupted, truncated response: {original}")
#     conversation_history.append(f"Agent (interrupted): {original}")

# def on_user_transcript(transcript):
#     print(f"User: {transcript}")
#     conversation_history.append(f"User: {transcript}")

# # NEW: Callback to handle tool calls from the AI
# def handle_tool_call(tool_call: ToolCall):
#     """
#     This function is the 'dispatcher'. It gets called when the AI decides to use a tool.
#     It looks up the correct Python function from our `tool_map` and executes it
#     with the arguments provided by the AI.
#     """
#     print(f"AI is attempting to use tool: {tool_call.name} with arguments: {tool_call.arguments}")

#     # Look up the function in our map
#     if tool_call.name in tool_map:
#         func = tool_map[tool_call.name]
#         try:
#             # Execute the function with the arguments provided by the AI
#             result = func(**tool_call.arguments)
#         except Exception as e:
#             result = f"Error executing tool {tool_call.name}: {e}"

#         print(f"Tool execution result: {result}")
#         # Send the result back to the AI
#         tool_call.respond(result)
#     else:
#         print(f"Error: AI tried to call an unknown tool '{tool_call.name}'")
#         tool_call.respond(f"Error: The tool '{tool_call.name}' is not available.")


# # --- Main Application Execution ---

# # NEW: Add the `on_tool_call` handler to the Conversation object
# conversation = Conversation(
#     client,
#     AGENT_ID,
#     config=config,
#     requires_auth=True,
#     audio_interface=DefaultAudioInterface(),
#     callback_agent_response=on_agent_response,
#     callback_agent_response_correction=on_interrupted_response,
#     callback_user_transcript=on_user_transcript,
#     on_tool_call=handle_tool_call,  # <-- This is the new, crucial part
# )

# print("\n--- Starting Conversation ---")
# print("You can now speak to the assistant. Press Ctrl+C to end.")

# try:
#     conversation.start_session()
# except KeyboardInterrupt:
#     print("\nConversation ended by user.")
# finally:
#     print("\n--- Full Conversation Transcript ---")
#     for line in conversation_history:
#         print(line)

import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# --- Environment Setup ---
load_dotenv()

# Load ElevenLabs API Key and Agent ID from environment variables
# Ensure you have a .env file with:
# AGENT_ID="your_agent_id"
# API_KEY="your_elevenlabs_api_key"
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# Define the database path
DB_PATH = "ORDER.db"

# --- Database Setup and Sample Data Insertion (for demonstration) ---
def setup_database():
    """Creates the database and populates it with sample data if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        address TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL NOT NULL,
        status TEXT CHECK(status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')) DEFAULT 'pending',
        shipping_address TEXT NOT NULL,
        fulfillment_threshold TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        return_status TEXT CHECK(return_status IN ('none', 'requested', 'approved', 'completed')) DEFAULT 'none',
        return_reason TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS returns (
        return_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        order_item_id INTEGER,
        customer_id INTEGER,
        return_reason TEXT,
        status TEXT CHECK(status IN ('initiated', 'approved', 'label_generated', 'completed')) DEFAULT 'initiated',
        return_label_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        features TEXT,
        price REAL NOT NULL,
        online_stock INTEGER DEFAULT 0,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        store_id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT,
        region TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store_inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        store_id INTEGER,
        stock_quantity INTEGER NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        status TEXT CHECK(status IN ('available', 'busy', 'offline')) DEFAULT 'available'
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        intent TEXT,
        escalation_status TEXT CHECK(escalation_status IN ('self_resolved', 'escalated', 'pending')) DEFAULT 'pending',
        agent_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        sender TEXT CHECK(sender IN ('customer', 'assistant')) NOT NULL,
        message_text TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
    )""")

    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        sample_customers = [
            ('John', 'Smith', 'john.smith@email.com', '123 Main St, Anytown', '555-1234'),
            ('Jane', 'Doe', 'jane.doe@email.com', '456 Oak Ave, Otherville', '555-5678'),
            ('Peter', 'Jones', 'peter.jones@email.com', '789 Pine Ln, Somewhere', '555-9012')
        ]
        cursor.executemany("INSERT INTO customers (first_name, last_name, email, address, phone) VALUES (?, ?, ?, ?, ?)", sample_customers)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Wireless Headphones', 'High-quality wireless headphones', 'Bluetooth, Noise Cancelling', 99.99, 50, 'Electronics'),
            ('Laptop Pro', 'Powerful laptop for professionals', '16GB RAM, 512GB SSD', 1200.00, 25, 'Computers'),
            ('Ergonomic Chair', 'Comfortable chair for long working hours', 'Adjustable height, Lumbar support', 250.00, 100, 'Furniture'),
            ('Smartphone X', 'Latest model smartphone', 'OLED Display, 128GB Storage', 799.99, 75, 'Electronics')
        ]
        cursor.executemany("INSERT INTO products (name, description, features, price, online_stock, category) VALUES (?, ?, ?, ?, ?, ?)", sample_products)

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        now = datetime.now()
        sample_orders = [
            (1, now - timedelta(days=3), 250.00, 'shipped', '123 Main St, Anytown', now + timedelta(days=7)), # Order 101
            (2, now - timedelta(days=5), 799.99, 'delivered', '456 Oak Ave, Otherville', now + timedelta(days=5)), # Order 102
            (1, now - timedelta(days=1), 1300.00, 'pending', '999 New St, LA', now + timedelta(days=10)), # Order 103
            (3, now - timedelta(days=2), 99.99, 'confirmed', '789 Pine Ln, Somewhere', now + timedelta(days=15)), # Order 104
            (2, now - timedelta(days=6), 1200.00, 'shipped', '456 Oak Ave, Otherville', now + timedelta(days=4)), # Order 105 (past threshold)
            (1, now - timedelta(days=1), 250.00, 'pending', '123 Main St, Anytown', now + timedelta(days=8)), # Order 106
            (3, now - timedelta(days=7), 799.99, 'confirmed', '789 Pine Ln, Somewhere', now + timedelta(days=2)), # Order 107 (past threshold)
            (1, now - timedelta(days=4), 100.00, 'pending', '123 Main St, Anytown', now + timedelta(days=12)) # Order 108
        ]
        cursor.executemany("INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address, fulfillment_threshold) VALUES (?, ?, ?, ?, ?, ?)", sample_orders)

    cursor.execute("SELECT COUNT(*) FROM order_items")
    if cursor.fetchone()[0] == 0:
        sample_order_items = [
            (101, 1, 1, 1, 250.00, 'none', None), # Ergonomic Chair for Order 101
            (102, 2, 4, 1, 799.99, 'none', None), # Smartphone X for Order 102
            (103, 1, 2, 1, 1200.00, 'none', None), # Laptop Pro for Order 103
            (104, 3, 1, 1, 99.99, 'none', None), # Wireless Headphones for Order 104 (damaged)
            (105, 2, 2, 1, 1200.00, 'none', None), # Laptop Pro for Order 105
            (106, 1, 3, 1, 250.00, 'none', None), # Ergonomic Chair for Order 106
            (107, 3, 4, 1, 799.99, 'none', None), # Smartphone X for Order 107
            (108, 1, 1, 1, 99.99, 'none', None) # Wireless Headphones for Order 108
        ]
        cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity, unit_price, return_status, return_reason) VALUES (?, ?, ?, ?, ?, ?)", sample_order_items)

    cursor.execute("SELECT COUNT(*) FROM returns")
    if cursor.fetchone()[0] == 0:
        sample_returns = [
            (104, 4, 3, 'damaged', 'initiated', 'http://example.com/return/label/12345'), # Return for Order 104 item 4
            (105, 5, 2, 'incorrect_item', 'initiated', 'http://example.com/return/label/67890') # Return for Order 105 item 5
        ]
        cursor.executemany("INSERT INTO returns (order_id, order_item_id, customer_id, return_reason, status, return_label_url) VALUES (?, ?, ?, ?, ?, ?)", sample_returns)
        # Update order_items return status for created returns
        for ret in sample_returns:
            order_id, order_item_id, _, _, _, _ = ret
            cursor.execute("UPDATE order_items SET return_status = 'requested', return_reason = ? WHERE order_id = ? AND order_item_id = ?", ('damaged', order_id, order_item_id)) # Assuming return_reason is passed

    cursor.execute("SELECT COUNT(*) FROM stores")
    if cursor.fetchone()[0] == 0:
        sample_stores = [
            ('New York Store', '100 Broadway, New York', '212-555-0100', 'East'),
            ('Los Angeles Store', '200 Sunset Blvd, Los Angeles', '310-555-0200', 'West'),
            ('Chicago Store', '300 Michigan Ave, Chicago', '312-555-0300', 'Midwest')
        ]
        cursor.executemany("INSERT INTO stores (store_name, address, phone, region) VALUES (?, ?, ?, ?)", sample_stores)

    cursor.execute("SELECT COUNT(*) FROM store_inventory")
    if cursor.fetchone()[0] == 0:
        sample_store_inventory = [
            (1, 1, 10), # Headphones in New York
            (1, 2, 5),  # Laptop Pro in New York
            (2, 4, 3),  # Smartphone X in Los Angeles
            (3, 3, 20)  # Ergonomic Chair in Chicago
        ]
        cursor.executemany("INSERT INTO store_inventory (product_id, store_id, stock_quantity) VALUES (?, ?, ?)", sample_store_inventory)

    cursor.execute("SELECT COUNT(*) FROM faq")
    if cursor.fetchone()[0] == 0:
        sample_faq = [
            ('Where is my order?', 'You can track your order status by providing your order ID. For detailed tracking information, please visit the "Track Order" section on our website.'),
            ('What is your return policy?', 'We accept returns within 30 days of purchase for most items. Items must be in their original condition. Please visit our Returns page for more details and to initiate a return.'),
            ('How can I contact customer support?', 'You can reach our customer support team via email at support@echosolve.com or by calling us at 1-800-ECHO-SOLVE. For immediate assistance, you can also use our live chat feature.')
        ]
        cursor.executemany("INSERT INTO faq (question, answer, category) VALUES (?, ?, ?)", sample_faq)

    cursor.execute("SELECT COUNT(*) FROM agents")
    if cursor.fetchone()[0] == 0:
        sample_agents = [
            ('Alice Carter', 'alice.carter@echosolve.com', 'available'),
            ('Bob Williams', 'bob.williams@echosolve.com', 'available')
        ]
        cursor.executemany("INSERT INTO agents (name, email, status) VALUES (?, ?, ?)", sample_agents)

    conn.commit()
    conn.close()

# --- Database Interaction Functions ---
def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def log_message(conversation_id, sender, message_text):
    """Logs a message to the conversation_messages table."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO conversation_messages (conversation_id, sender, message_text)
        VALUES (?, ?, ?)
        """, (conversation_id, sender, message_text))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging message: {e}")
    finally:
        conn.close()

def create_conversation(customer_id, intent=None):
    """Creates a new conversation record."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (customer_id, intent) VALUES (?, ?)", (customer_id, intent))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating conversation: {e}")
        return None
    finally:
        conn.close()

def update_conversation_intent(conversation_id, intent):
    """Updates the intent for an existing conversation."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET intent = ? WHERE conversation_id = ?", (intent, conversation_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating conversation intent: {e}")
    finally:
        conn.close()

def update_conversation_escalation_status(conversation_id, status, agent_id=None):
    """Updates the escalation status and optionally assigns an agent."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET escalation_status = ?, agent_id = ?, end_time = CURRENT_TIMESTAMP WHERE conversation_id = ?", (status, agent_id, conversation_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating conversation escalation status: {e}")
    finally:
        conn.close()

def get_available_agent():
    """Finds an available agent."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT agent_id FROM agents WHERE status = 'available' LIMIT 1")
        agent = cursor.fetchone()
        return agent['agent_id'] if agent else None
    except sqlite3.Error as e:
        print(f"Error getting available agent: {e}")
        return None
    finally:
        conn.close()

# --- Feature 1: Automated Order Modification ---
def modify_order(order_id, new_address=None, cancel_order=False):
    """Handles order modification requests."""
    conn = get_db_connection()
    if not conn:
        return "Sorry, I couldn't connect to the database to process your request."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status, fulfillment_threshold FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            return f"Order ID {order_id} not found."

        current_time = datetime.now()
        fulfillment_threshold = datetime.fromisoformat(order['fulfillment_threshold']) if order['fulfillment_threshold'] else current_time - timedelta(seconds=1) # Default to past if null

        if order['status'] in ['shipped', 'delivered', 'cancelled']:
            return f"Order {order_id} cannot be modified as it has already been {order['status']}."
        if current_time > fulfillment_threshold:
            return f"Order {order_id} has passed its fulfillment threshold and cannot be modified."

        if new_address:
            cursor.execute("UPDATE orders SET shipping_address = ?, updated_at = CURRENT_TIMESTAMP WHERE order_id = ?", (new_address, order_id))
            return f"Your delivery address for order {order_id} has been updated to {new_address}."
        elif cancel_order:
            cursor.execute("UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE order_id = ?", (order_id,))
            return f"Your order {order_id} has been successfully cancelled."
        else:
            return "Please specify what modification you would like to make (e.g., change address or cancel)."

    except sqlite3.Error as e:
        return f"An error occurred while modifying order {order_id}: {e}"
    finally:
        conn.close()

# --- Feature 2: Voice-Initiated Returns & Exchange Workflow ---
def initiate_return(order_id, order_item_id=None, return_reason=None):
    """Handles return and exchange requests."""
    conn = get_db_connection()
    if not conn:
        return "Sorry, I couldn't connect to the database to process your request."

    try:
        cursor = conn.cursor()

        # Verify order exists
        cursor.execute("SELECT customer_id, status FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        if not order:
            return f"Order ID {order_id} not found."

        # If order_item_id is not provided, try to find an eligible item for the order
        if order_item_id is None:
            cursor.execute("""
            SELECT oi.order_item_id, oi.return_status, p.name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ? AND oi.return_status = 'none'
            LIMIT 1
            """, (order_id,))
            item_data = cursor.fetchone()
            if item_data:
                order_item_id = item_data['order_item_id']
                product_name = item_data['name']
            else:
                return f"No eligible items found for return in order {order_id}."
        else:
            # Verify specific order item exists and is eligible
            cursor.execute("SELECT return_status, order_id FROM order_items WHERE order_item_id = ? AND order_id = ?", (order_item_id, order_id))
            item_data = cursor.fetchone()
            if not item_data:
                return f"Order item ID {order_item_id} not found for order {order_id}."
            if item_data['return_status'] != 'none':
                return f"Item {order_item_id} from order {order_id} has already been processed for return (status: {item_data['return_status']})."

            cursor.execute("SELECT p.name FROM order_items oi JOIN products p ON oi.product_id = p.product_id WHERE oi.order_item_id = ?", (order_item_id,))
            product_data = cursor.fetchone()
            product_name = product_data['name'] if product_data else "the item"


        if not return_reason:
            return "Please provide a reason for the return."

        # Check if a return has already been initiated for this item
        cursor.execute("SELECT return_id, status FROM returns WHERE order_id = ? AND order_item_id = ?", (order_id, order_item_id))
        existing_return = cursor.fetchone()

        if existing_return:
            if existing_return['status'] == 'initiated':
                return f"A return for item {order_item_id} in order {order_id} is already initiated. Status: {existing_return['status']}."
            elif existing_return['status'] in ['approved', 'label_generated', 'completed']:
                return f"This item from order {order_id} has already been processed for return. Status: {existing_return['status']}."

        # Create return record
        return_label_url = f"http://echosolve.com/return/label/{uuid.uuid4()}" # Simulate label generation
        cursor.execute("""
        INSERT INTO returns (order_id, order_item_id, customer_id, return_reason, status, return_label_url, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (order_id, order_item_id, order['customer_id'], return_reason, 'initiated', return_label_url))
        conn.commit()

        # Update order_items return status
        cursor.execute("UPDATE order_items SET return_status = 'requested', return_reason = ?, updated_at = CURRENT_TIMESTAMP WHERE order_item_id = ?", (return_reason, order_item_id))
        conn.commit()

        return f"Your return request for {product_name} from order {order_id} has been initiated due to '{return_reason}'. You can use this return label URL: {return_label_url}"

    except sqlite3.Error as e:
        return f"An error occurred while processing your return request for order {order_id}: {e}"
    finally:
        conn.close()

# --- Feature 3: Real-time Product Information & Store Inventory Lookup ---
def lookup_product_info(product_name_query=None, product_id=None):
    """Retrieves product details."""
    conn = get_db_connection()
    if not conn:
        return "Sorry, I couldn't connect to the database to fetch product information."

    try:
        cursor = conn.cursor()
        query_params = []
        sql_query = "SELECT product_id, name, description, features, price, online_stock FROM products WHERE "

        if product_name_query:
            sql_query += "LOWER(name) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?) OR LOWER(features) LIKE LOWER(?)"
            query_params.extend([f"%{product_name_query}%", f"%{product_name_query}%", f"%{product_name_query}%"])
        elif product_id:
            sql_query += "product_id = ?"
            query_params.append(product_id)
        else:
            return "Please specify a product name or ID to look up."

        cursor.execute(sql_query, tuple(query_params))
        product = cursor.fetchone()

        if not product:
            return f"I couldn't find any product matching your query '{product_name_query or product_id}'."

        response = f"Here is the information for {product['name']}: "
        response += f"Description: {product['description']}. "
        response += f"Features: {product['features']}. "
        response += f"Price: ${product['price']:.2f}. "
        response += f"Online Stock: {product['online_stock']} units available."
        return response

    except sqlite3.Error as e:
        return f"An error occurred while looking up product information: {e}"
    finally:
        conn.close()

def lookup_store_inventory(product_query, store_query):
    """Retrieves product inventory at specific store locations."""
    conn = get_db_connection()
    if not conn:
        return "Sorry, I couldn't connect to the database to check store inventory."

    try:
        cursor = conn.cursor()
        product_id = None
        store_id = None

        # Find product ID
        cursor.execute("SELECT product_id FROM products WHERE LOWER(name) LIKE LOWER(?)", (f"%{product_query}%",))
        product = cursor.fetchone()
        if product:
            product_id = product['product_id']
        else:
            return f"I couldn't find a product named '{product_query}'."

        # Find store ID
        cursor.execute("SELECT store_id FROM stores WHERE LOWER(store_name) LIKE LOWER(?) OR LOWER(address) LIKE LOWER(?)", (f"%{store_query}%", f"%{store_query}%"))
        store = cursor.fetchone()
        if store:
            store_id = store['store_id']
        else:
            return f"I couldn't find a store matching '{store_query}'."

        # Get inventory
        cursor.execute("""
        SELECT si.stock_quantity, p.name, s.store_name
        FROM store_inventory si
        JOIN products p ON si.product_id = p.product_id
        JOIN stores s ON si.store_id = s.store_id
        WHERE si.product_id = ? AND si.store_id = ?
        """, (product_id, store_id))
        inventory_data = cursor.fetchone()

        if not inventory_data:
            return f"No inventory information available for {product_query} at {store_query}."

        if inventory_data['stock_quantity'] > 0:
            return f"{product_query} is available at {inventory_data['store_name']} with {inventory_data['stock_quantity']} units in stock."
        else:
            return f"{product_query} is currently out of stock at {inventory_data['store_name']}."

    except sqlite3.Error as e:
        return f"An error occurred while checking store inventory: {e}"
    finally:
        conn.close()

# --- Feature 4: Intelligent Triage & Self-Service Resolution ---
def handle_triage(message_text, current_conversation_id, customer_id):
    """Handles common queries, provides self-service answers, or escalates."""
    conn = get_db_connection()
    if not conn:
        return "Sorry, I couldn't connect to the database to process your request.", 'self_resolved'

    try:
        cursor = conn.cursor()
        message_text_lower = message_text.lower()

        # --- Intent Detection (Rule-based for simplicity) ---

        # Order Status Query
        if "where is my order" in message_text_lower or "order status" in message_text_lower or "track my order" in message_text_lower:
            order_id_match = None
            for word in message_text.split():
                if word.isdigit():
                    try:
                        order_id = int(word)
                        cursor.execute("SELECT order_id, status FROM orders WHERE order_id = ?", (order_id,))
                        order = cursor.fetchone()
                        if order:
                            order_id_match = order_id
                            return f"The status of order {order_id} is: {order['status']}.", 'self_resolved'
                    except ValueError:
                        pass # Not a valid integer
            if order_id_match is None:
                return "Please provide your order ID so I can check its status.", 'self_resolved'

        # Return Policy Query
        if "return policy" in message_text_lower or "how to return" in message_text_lower:
            cursor.execute("SELECT answer FROM faq WHERE LOWER(question) LIKE LOWER(?)", ('%return policy%',))
            faq_entry = cursor.fetchone()
            if faq_entry:
                return faq_entry['answer'], 'self_resolved'
            else:
                return "Our return policy allows returns within 30 days of purchase for most items. Please visit our website for detailed information.", 'self_resolved'

        # Product Query (fallback for general product info)
        if "tell me about" in message_text_lower or "what is" in message_text_lower or "show me" in message_text_lower:
            # Extract product name
            product_name_parts = []
            if "tell me about" in message_text_lower:
                product_name_parts = message_text.split("tell me about", 1)[1].strip().split("?")[0].strip()
            elif "what is" in message_text_lower:
                product_name_parts = message_text.split("what is", 1)[1].strip().split("?")[0].strip()
            elif "show me" in message_text_lower:
                product_name_parts = message_text.split("show me", 1)[1].strip().split("?")[0].strip()

            if product_name_parts:
                return lookup_product_info(product_name_query=product_name_parts), 'self_resolved'
            else:
                return "What product are you interested in?", 'self_resolved'


        # Inventory Query
        if "in stock" in message_text_lower or "do you have" in message_text_lower:
            # Attempt to parse product and store
            product_query = None
            store_query = None
            parts = message_text.lower().split()
            for i, part in enumerate(parts):
                if part == "in" and parts[i-1] == "stock":
                    product_query = " ".join(parts[:i-1])
                    break
                if part == "have" and i + 1 < len(parts):
                    product_query = " ".join(parts[parts.index("do") + 1:i])
                    store_query = " ".join(parts[i+1:]).replace("?", "").strip()
                    break
                if part == "stock" and i > 0: # "stock in new york" style
                    product_query = " ".join(parts[:parts.index(part)-1])
                    store_query = " ".join(parts[parts.index(part)+2:])
                    break
                if part == "in" and i > 0 and parts[i-1] in ["new york", "los angeles", "chicago"]: # handle specific store names
                    store_query = parts[i-1]
                    product_query = " ".join(parts[:i-1])
                    break


            if product_query and store_query:
                return lookup_store_inventory(product_query, store_query), 'self_resolved'
            elif product_query:
                return lookup_product_info(product_query), 'self_resolved' # Fallback to online stock
            else:
                return "What product are you looking for and at which store?", 'self_resolved'


        # Generic or unhandled queries that might require escalation
        # For simplicity, we'll escalate anything not explicitly handled as self-resolved
        # In a real system, you'd have more sophisticated intent matching and self-service flow.

        # Try to find an available agent
        agent_id = get_available_agent()
        if agent_id:
            # Fetch last few messages for context
            cursor.execute("""
            SELECT message_text, sender FROM conversation_messages
            WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT 5
            """, (current_conversation_id,))
            recent_messages = cursor.fetchall()
            context = "\n".join([f"{msg['sender'].capitalize()}: {msg['message_text']}" for msg in recent_messages[::-1]])

            response_message = (
                f"This query seems complex. I'm escalating it to a human agent. "
                f"Please wait while I connect you. Here's the context of our conversation:\n{context}"
            )
            update_conversation_escalation_status(current_conversation_id, 'escalated', agent_id)
            return response_message, 'escalated'
        else:
            return "I'm sorry, I can't seem to find an available agent right now. Please try again later.", 'self_resolved'

    except sqlite3.Error as e:
        print(f"Database error in triage: {e}")
        return "An internal error occurred. Please try again.", 'self_resolved'
    finally:
        conn.close()

# --- ElevenLabs Callbacks ---
# Global variable to store the current conversation ID
current_conversation_id_global = None
current_customer_id_global = 1 # Default customer for simplicity, ideally passed from user login/context

def print_agent_response(response):
    """Callback to print agent's response and log it."""
    global current_conversation_id_global
    print(f"Agent: {response}")
    if current_conversation_id_global:
        log_message(current_conversation_id_global, 'assistant', response)

def print_interrupted_response(original, corrected):
    """Callback for interrupted agent responses."""
    global current_conversation_id_global
    print(f"Agent interrupted, corrected response: {corrected}")
    if current_conversation_id_global:
        log_message(current_conversation_id_global, 'assistant', f"[Interrupted: {corrected}]")

def print_user_transcript(transcript):
    """Callback to print user's transcript and log it."""
    global current_conversation_id_global
    print(f"User: {transcript}")
    if current_conversation_id_global:
        log_message(current_conversation_id_global, 'customer', transcript)

    # --- Core Logic: Processing user transcript to determine intent and response ---
    global current_customer_id_global

    # First message of a new conversation or after escalation reset
    if not current_conversation_id_global:
        current_conversation_id_global = create_conversation(current_customer_id_global)
        if not current_conversation_id_global:
            print("Error: Failed to create a new conversation.")
            return

    response_message = ""
    intent = None

    # Feature 1: Order Modification
    if "change my delivery address" in transcript.lower() or "cancel my order" in transcript.lower():
        intent = 'order_modification'
        update_conversation_intent(current_conversation_id_global, intent)
        order_id = None
        new_address = None
        cancel_order = False

        # Parse for order ID
        for word in transcript.split():
            if word.isdigit():
                try:
                    order_id = int(word)
                    break
                except ValueError:
                    pass

        # Parse for address change
        if "change my delivery address to" in transcript.lower():
            parts = transcript.lower().split("change my delivery address to", 1)
            if len(parts) > 1:
                new_address = parts[1].strip().rstrip('.').strip()
        elif "cancel my order" in transcript.lower():
            cancel_order = True

        if order_id:
            response_message = modify_order(order_id, new_address, cancel_order)
        else:
            response_message = "I need your order ID to proceed with the modification. Please tell me the order ID."

    # Feature 2: Returns & Exchanges
    elif "return order" in transcript.lower() or "exchange for" in transcript.lower():
        intent = 'return_request'
        update_conversation_intent(current_conversation_id_global, intent)
        order_id = None
        return_reason = None
        order_item_id = None # Optional, if user specifies

        # Parse order ID
        for word in transcript.split():
            if word.isdigit():
                try:
                    order_id = int(word)
                    break
                except ValueError:
                    pass

        # Parse return reason
        if "damaged" in transcript.lower():
            return_reason = "damaged"
        elif "incorrect item" in transcript.lower() or "wrong item" in transcript.lower():
            return_reason = "incorrect_item"
        elif "defective" in transcript.lower():
            return_reason = "defective"
        else:
            # Try to extract reason if it's explicitly stated
            parts = transcript.lower().split("reason is")
            if len(parts) > 1:
                return_reason = parts[1].strip().rstrip('.').strip()
            elif "return" in transcript.lower():
                # Generic reason if not specified, to prompt user
                return_reason = "unspecified"


        # Attempt to parse order_item_id if mentioned (e.g., "return order 104 item 5")
        words = transcript.split()
        try:
            if "item" in words:
                item_index = words.index("item")
                if item_index + 1 < len(words) and words[item_index+1].isdigit():
                    order_item_id = int(words[item_index+1])
        except ValueError:
            pass


        if order_id:
            response_message = initiate_return(order_id, order_item_id, return_reason)
        else:
            response_message = "I need your order ID to process a return. Please provide the order ID."

    # Feature 3 & 4: Product Info, Inventory, Triage, and Escalation
    else:
        intent = 'triage_or_query'
        update_conversation_intent(current_conversation_id_global, intent)
        response_message, resolution_status = handle_triage(transcript, current_conversation_id_global, current_customer_id_global)

        if resolution_status == 'escalated':
            update_conversation_escalation_status(current_conversation_id_global, 'escalated', None) # Agent assigned internally by handle_triage
            current_conversation_id_global = None # Reset for a new conversation after escalation
        elif resolution_status == 'self_resolved':
            update_conversation_escalation_status(current_conversation_id_global, 'self_resolved')
            current_conversation_id_global = None # Reset for a new conversation


    # Send the determined response back to the ElevenLabs conversation
    # This requires overriding the default callback behavior for the agent's response
    # The `Conversation` object's `add_message` method will trigger the `callback_agent_response`
    # We need to manually trigger this logic here.

    # If a specific feature handler provided a response, use it. Otherwise, rely on the general triage.
    if response_message:
        # Use the client's text-to-speech to generate audio for the response
        # This is a workaround to simulate the agent speaking the response.
        # In a true streaming scenario, the conversation object handles this.
        try:
            tts_response = client.text_to_speech.convert(
                text=response_message,
                voice="pNjTzx96n0uB0d0Y88iH", # Example voice ID, replace with a suitable one
                model="eleven-turbo-v2",
            )
            # The actual audio playback or saving would happen here if we were managing audio directly.
            # For this simulation, we'll just print and log.
            print_agent_response(response_message)
        except Exception as e:
            print(f"Error generating TTS for response: {e}")
            print_agent_response(response_message) # Fallback to just printing if TTS fails

    else:
        # Fallback if no response was generated (should not happen with handle_triage)
        print_agent_response("I'm sorry, I didn't understand that. How can I help you?")


# --- Main Execution ---
def start_echoresolve():
    """Initializes and starts the EchoResolve conversational AI."""
    global current_conversation_id_global
    global current_customer_id_global

    setup_database() # Ensure DB and sample data are ready

    if not AGENT_ID or not API_KEY:
        print("Error: AGENT_ID and API_KEY must be set in the environment variables.")
        return

    try:
        client = ElevenLabs(api_key=API_KEY)

        # Define the prompt for EchoResolve
        prompt_text = """
        You are EchoResolve, an AI-powered voice assistant for real-time customer service.
        Your primary goal is to assist customers with their orders, product inquiries, and provide support.
        You can:
        1. Modify orders (update shipping address, cancel) if they are not yet shipped or past the fulfillment threshold.
        2. Guide customers through returns and exchanges for damaged or incorrect items, providing a return label URL.
        3. Provide real-time product information (features, price, online stock) and check store inventory at specific locations.
        4. Triage common customer queries (e.g., order status, return policy) using the FAQ and order data.
        5. Escalate complex or unresolvable issues to a human agent with conversation context.

        When a customer makes a request, first determine their intent. If the intent requires accessing or modifying data,
        query the SQLite database (ORDER.db) to retrieve or update information.
        Ensure all interactions are logged in the database.

        When responding, be clear, concise, and helpful. If you need more information (like an order ID), ask for it directly.
        If an action is successful, confirm it. If an action fails due to constraints (e.g., order already shipped), explain why.
        For returns, simulate a return label URL. For inventory, check both online and store stock.
        For triage, use the FAQ table for common questions. If a query cannot be resolved through self-service,
        identify an available human agent and provide the conversation context for escalation.
        """

        first_message = "Hello, welcome to EchoResolve. How can I assist you today?"

        conversation_override = {
            "agent": {
                "prompt": {
                    "prompt": prompt_text,
                },
                "first_message": first_message,
            },
        }

        config = ConversationConfig(
            conversation_config_override=conversation_override,
            extra_body={},
            dynamic_variables={},
        )

        conversation = Conversation(
            client,
            AGENT_ID,
            config=config,
            requires_auth=True,
            audio_interface=DefaultAudioInterface(),
            callback_agent_response=print_agent_response,
            callback_agent_response_correction=print_interrupted_response,
            callback_user_transcript=print_user_transcript,
        )

        print("EchoResolve starting... Say 'Hello' to begin.")
        # The conversation.start_session() will handle listening for user input
        # and invoking callbacks. Our logic to process transcripts is within
        # print_user_transcript.
        conversation.start_session()

    except Exception as e:
        print(f"An error occurred during EchoResolve initialization: {e}")

if __name__ == "__main__":
    # Replace 'YOUR_UNIQUE_UUID' with an actual UUID generated for this artifact.
    # For demonstration purposes, we'll keep it as a placeholder.
    # In a real scenario, you'd generate it once: str(uuid.uuid4())
    print(f"Starting EchoResolve application...\n")
    start_echoresolve()
