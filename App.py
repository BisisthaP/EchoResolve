# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # AGENT_ID = os.getenv("AGENT_ID")
# # API_KEY = os.getenv("API_KEY")

# # from elevenlabs.client import ElevenLabs
# # from elevenlabs.conversational_ai.conversation import Conversation
# # from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# # from elevenlabs.types import ConversationConfig

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
# # conversation = Conversation(
# #     client,
# #     AGENT_ID,
# #     config=config,
# #     requires_auth=True,
# #     audio_interface=DefaultAudioInterface(),
# # )


# # def print_agent_response(response):
# #     print(f"Agent: {response}")


# # def print_interrupted_response(original, corrected):
# #     print(f"Agent interrupted, truncated response: {corrected}")


# # def print_user_transcript(transcript):
# #     print(f"User: {transcript}")


# # conversation = Conversation(
# #     client,
# #     AGENT_ID,
# #     config=config,
# #     requires_auth=True,
# #     audio_interface=DefaultAudioInterface(),
# #     callback_agent_response=print_agent_response,
# #     callback_agent_response_correction=print_interrupted_response,
# #     callback_user_transcript=print_user_transcript,
# # )

# # conversation.start_session()

# import os
# from dotenv import load_dotenv

# load_dotenv()

# AGENT_ID = os.getenv("AGENT_ID")
# API_KEY = os.getenv("API_KEY")

# from elevenlabs.client import ElevenLabs
# from elevenlabs.conversational_ai.conversation import Conversation
# from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# from elevenlabs.types import ConversationConfig

# # This list will store the conversation transcript
# conversation_history = []

# user_name = "Alex"
# schedule = "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00"
# prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
# first_message = f"Hello {user_name}, how can I help you today?"

# conversation_override = {
#     "agent": {
#         "prompt": {
#             "prompt": prompt,
#         },
#         "first_message": first_message,
#     },
# }

# config = ConversationConfig(
#     conversation_config_override=conversation_override,
#     extra_body={},
#     dynamic_variables={},
# )

# client = ElevenLabs(api_key=API_KEY)

# def on_agent_response(response):
#     """Callback function to handle and store the agent's response."""
#     print(f"Agent: {response}")
#     conversation_history.append(f"Agent: {response}")

# def on_interrupted_response(original, corrected):
#     """Callback function to handle interrupted agent responses."""
#     print(f"Agent interrupted, truncated response: {original}")
#     # You might want to decide how to log interruptions
#     conversation_history.append(f"Agent (interrupted): {original}")


# def on_user_transcript(transcript):
#     """Callback function to handle and store the user's transcript."""
#     print(f"User: {transcript}")
#     conversation_history.append(f"User: {transcript}")


# conversation = Conversation(
#     client,
#     AGENT_ID,
#     config=config,
#     requires_auth=True,
#     audio_interface=DefaultAudioInterface(),
#     callback_agent_response=on_agent_response,
#     callback_agent_response_correction=on_interrupted_response,
#     callback_user_transcript=on_user_transcript,
# )

# try:
#     conversation.start_session()
#     # The conversation will run here until it's ended by the user
#     # or another condition.

# except KeyboardInterrupt:
#     print("\nConversation ended by user.")

# finally:
#     # You can now access the full transcript
#     print("\n--- Full Conversation Transcript ---")
#     for line in conversation_history:
#         print(line)
import os
import sqlite3
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ToolCall
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# --- Configuration and Setup ---
load_dotenv()
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")
DB_FILE = "sample_orders.db"
conversation_history = []

# --- 1. Database Functions (The "Tools") ---
# These functions contain the actual business logic and interact with the database.

def db_connect():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def get_order_status(order_id: str) -> str:
    """Fetches the status of a specific order from the database."""
    print(f"DATABASE: Checking status for order_id: {order_id}")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            status, fulfillment = result
            return f"Success: Order {order_id} has a status of '{status}' and its fulfillment status is '{fulfillment}'."
        else:
            return f"Error: Order with ID '{order_id}' was not found."
    except Exception as e:
        return f"Error: A database error occurred: {e}"

def cancel_order(order_id: str) -> str:
    """Attempts to cancel an order if it has not yet been shipped."""
    print(f"DATABASE: Attempting to cancel order_id: {order_id}")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return f"Error: Order with ID '{order_id}' was not found."

        status, fulfillment = result
        # Business Rule: Cannot cancel if it's shipped, out for delivery, or already cancelled.
        if status in ['Shipped', 'Cancelled'] or fulfillment == 'Out for Delivery':
            conn.close()
            return f"Error: Cannot cancel order {order_id}. Its status is '{status}' and fulfillment is '{fulfillment}', which is past the cancellation window."

        cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()
        return f"Success: Order {order_id} has been successfully cancelled."
    except Exception as e:
        return f"Error: A database error occurred: {e}"

def update_delivery_address(order_id: str, new_address: str) -> str:
    """Updates the delivery address for an order if it has not been dispatched."""
    print(f"DATABASE: Attempting to update address for order_id: {order_id}")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, fulfillment_status FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return f"Error: Order with ID '{order_id}' was not found."

        status, fulfillment = result
        # Business Rule: Cannot change address if it's already on its way or shipped.
        if status in ['Shipped', 'Cancelled'] or fulfillment == 'Out for Delivery':
            conn.close()
            return f"Error: Cannot update address for order {order_id}. Its fulfillment status is '{fulfillment}', which is too late to change."

        cursor.execute("UPDATE orders SET shipping_address = ? WHERE order_id = ?", (new_address, order_id))
        conn.commit()
        conn.close()
        return f"Success: The delivery address for order {order_id} has been updated to '{new_address}'."
    except Exception as e:
        return f"Error: A database error occurred: {e}"

def initiate_order_return(order_id: str) -> str:
    """Initiates a return for an order if it has already been delivered or shipped."""
    print(f"DATABASE: Attempting to initiate return for order_id: {order_id}")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return f"Error: Order with ID '{order_id}' was not found."

        status = result 
        # Business Rule: Can only return an item that has been shipped.
        if status not in ['Shipped']:
             return f"Error: Cannot initiate a return for order {order_id}. The order status is '{status}'. Returns are only possible for shipped items."

        cursor.execute("UPDATE orders SET status = 'Return Initiated' WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()
        return f"Success: A return has been initiated for order {order_id}. Please check your email for instructions on how to proceed."
    except Exception as e:
        return f"Error: A database error occurred: {e}"

# --- 2. Tool Definitions ---
# This structure describes our Python functions to the AI.
# The 'description' is crucial for the AI to decide which tool to use.
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Use this tool to get the current status and fulfillment details of a customer's order. Ask for the order ID if the user does not provide it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The unique identifier for the order, e.g., '10'."},
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Use this tool to cancel a customer's order. It will only work if the order has not yet been shipped. Always confirm the order ID with the user before using this tool.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The unique identifier for the order to be cancelled, e.g., '10'."},
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_delivery_address",
            "description": "Use this tool to change the shipping address for an order. This is only possible before the order is dispatched. You must get both the order ID and the new, complete address from the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The unique identifier for the order."},
                    "new_address": {"type": "string", "description": "The full new shipping address."},
                },
                "required": ["order_id", "new_address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "initiate_order_return",
            "description": "Use this tool to start the return process for an order that has already been shipped. Inform the user that they will receive further instructions via email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The unique identifier for the order to be returned."},
                },
                "required": ["order_id"],
            },
        },
    }
]

# A mapping from the function name (string) to the actual Python function object.
tool_map = {
    "get_order_status": get_order_status,
    "cancel_order": cancel_order,
    "update_delivery_address": update_delivery_address,
    "initiate_order_return": initiate_order_return,
}

# --- 3. Conversational AI Configuration & Callbacks ---

# NEW: Updated Prompt and First Message
user_name = "Alex"
prompt = (
    "You are a friendly and highly capable customer service assistant. "
    "Your primary role is to help users manage their orders using the provided tools. "
    "Always be polite and clear. If you need information like an order ID, ask for it clearly. "
    "When an action is successful or fails, clearly state the outcome to the user based on the tool's response."
)
first_message = f"Hello {user_name}, how can I help you today? You can ask about your schedule or manage a recent order."

# NEW: Add the tool definitions to the conversation configuration
conversation_override = {
    "agent": {
        "prompt": {"prompt": prompt},
        "first_message": first_message,
        "tools": tool_definitions,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
)

client = ElevenLabs(api_key=API_KEY)

# Transcript callbacks (unchanged)
def on_agent_response(response):
    print(f"Agent: {response}")
    conversation_history.append(f"Agent: {response}")

def on_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {original}")
    conversation_history.append(f"Agent (interrupted): {original}")

def on_user_transcript(transcript):
    print(f"User: {transcript}")
    conversation_history.append(f"User: {transcript}")

# NEW: Callback to handle tool calls from the AI
def handle_tool_call(tool_call: ToolCall):
    """
    This function is the 'dispatcher'. It gets called when the AI decides to use a tool.
    It looks up the correct Python function from our `tool_map` and executes it
    with the arguments provided by the AI.
    """
    print(f"AI is attempting to use tool: {tool_call.name} with arguments: {tool_call.arguments}")

    # Look up the function in our map
    if tool_call.name in tool_map:
        func = tool_map[tool_call.name]
        try:
            # Execute the function with the arguments provided by the AI
            result = func(**tool_call.arguments)
        except Exception as e:
            result = f"Error executing tool {tool_call.name}: {e}"

        print(f"Tool execution result: {result}")
        # Send the result back to the AI
        tool_call.respond(result)
    else:
        print(f"Error: AI tried to call an unknown tool '{tool_call.name}'")
        tool_call.respond(f"Error: The tool '{tool_call.name}' is not available.")


# --- Main Application Execution ---

# NEW: Add the `on_tool_call` handler to the Conversation object
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=on_agent_response,
    callback_agent_response_correction=on_interrupted_response,
    callback_user_transcript=on_user_transcript,
    on_tool_call=handle_tool_call,  # <-- This is the new, crucial part
)

print("\n--- Starting Conversation ---")
print("You can now speak to the assistant. Press Ctrl+C to end.")

try:
    conversation.start_session()
except KeyboardInterrupt:
    print("\nConversation ended by user.")
finally:
    print("\n--- Full Conversation Transcript ---")
    for line in conversation_history:
        print(line)
