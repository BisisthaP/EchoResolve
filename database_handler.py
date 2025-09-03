import sqlite3
import re

DB_NAME = "sample_orders.db"

def extract_order_id(text: str) -> int | None:
    """Uses regex to find the first sequence of digits in a string."""
    match = re.search(r'\d+', text)
    if match:
        return int(match.group(0))
    return None

def process_return_for_order(order_id: int) -> str:
    """
    Processes a return for a given order_id.

    Returns:
        A string message indicating success or failure, to be sent to the LLM.
    """
    if not isinstance(order_id, int):
        return "FAILURE: The order ID provided was invalid."

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 1. Check if the order exists
        cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()

        if result is None:
            return f"FAILURE: Order with ID {order_id} could not be found."

        current_status = result[0]

        # 2. Check if the order is eligible for return
        if current_status in ["Returned", "Cancelled", "Pending"]:
            return f"FAILURE: Order {order_id} is not eligible for a return because its status is '{current_status}'."

        # 3. Update the order status to 'Returned'
        cursor.execute("UPDATE orders SET status = 'Returned' WHERE order_id = ?", (order_id,))
        conn.commit()

        return f"SUCCESS: The return for order {order_id} has been processed successfully."

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "FAILURE: A database error occurred while processing the return."
    finally:
        if conn:
            conn.close()