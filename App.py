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

# import os
# from dotenv import load_dotenv

# # Load environment variables from a .env file
# load_dotenv()

# # --- Configuration ---
# # Make sure you have a .env file in the same directory with these variables
# AGENT_ID = os.getenv("ELEVEN_AGENT_ID")
# API_KEY = os.getenv("ELEVEN_API_KEY")

# # Check if the environment variables are loaded correctly
# if not AGENT_ID or not API_KEY:
#     raise ValueError("ELEVEN_AGENT_ID and ELEVEN_API_KEY must be set in your .env file.")

# from elevenlabs.client import ElevenLabs
# from elevenlabs.conversational_ai.conversation import Conversation
# from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
# from elevenlabs.types import ConversationConfig

# # --- 1. Updated Prompt for a Customer Support Agent ---
# # This prompt defines the agent's role, capabilities, and personality.
# prompt = (
#     "You are a friendly, patient, and professional customer support agent for a company named 'Aurora Commerce'. "
#     "Your primary role is to assist users with two specific tasks: processing returns and handling order cancellations. "
#     "When a user asks for help, greet them warmly and ask how you can assist. "
#     "If they mention 'return' or 'cancellation', guide them through the necessary steps. "
#     "For returns, you will need to ask for their order number to begin the process. "
#     "For cancellations, you will also ask for the order number to check the order's status. "
#     "Remain focused on these tasks. If the user asks something outside of this scope, politely state that you can only help with returns and cancellations."
# )

# # The first message the agent will speak to the user.
# first_message = "Thank you for calling Aurora Commerce. How can I help you today?"

# # --- Configuration Overrides for the Session ---
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

# # Initialize the ElevenLabs client
# client = ElevenLabs(api_key=API_KEY)

# # --- Callback Functions ---

# def print_agent_response(response):
#     """Prints the agent's full text response."""
#     print(f"Agent: {response}")

# def print_interrupted_response(original, corrected):
#     """Handles cases where the agent is interrupted."""
#     print(f"Agent interrupted, truncated response: {corrected}")

# # --- 2. Function to Capture and Analyze the User Transcript ---
# def process_user_transcript(transcript):
#     """
#     This function is called every time the user finishes speaking.
#     It prints the transcript and checks for keywords.
#     """
#     print(f"User: {transcript}")
    
#     # Check for the keyword "return" in the user's speech (case-insensitive)
#     if "return" in transcript.lower():
#         # This is where you would trigger your custom function for handling returns
#         print("\n>>> SYSTEM: Keyword 'return' detected. Initiating return process logic... <<<\n")
    
#     # You can add more keyword checks here
#     if "cancel" in transcript.lower():
#         print("\n>>> SYSTEM: Keyword 'cancel' detected. Initiating cancellation process logic... <<<\n")


# # --- Initialize and Start the Conversation ---
# # This single, correct initialization sets up the conversation with all callbacks.
# try:
#     print("Starting conversation... Press Ctrl+C to exit.")
#     conversation = Conversation(
#         client,
#         AGENT_ID,
#         config=config,
#         requires_auth=True,
#         audio_interface=DefaultAudioInterface(),
#         callback_agent_response=print_agent_response,
#         callback_agent_response_correction=print_interrupted_response,
#         callback_user_transcript=process_user_transcript, # Use our new function here
#     )

#     # Start the conversation session. This will begin listening to the microphone.
#     conversation.start_session()

# except Exception as e:
#     print(f"An error occurred: {e}")

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# --- Import our database handler functions ---
from database_handler import process_return_for_order, extract_order_id

# Load environment variables
load_dotenv()
AGENT_ID = os.getenv("ELEVEN_AGENT_ID")
API_KEY = os.getenv("ELEVEN_API_KEY")
if not AGENT_ID or not API_KEY:
    raise ValueError("ELEVEN_AGENT_ID and ELEVEN_API_KEY must be set in your .env file.")

# --- 1. State Management ---
class ConversationManager:
    """Manages the state of the conversation."""
    def __init__(self):
        self.state = "IDLE"  # Possible states: IDLE, AWAITING_ORDER_ID_FOR_RETURN
        self.conversation = None

    def set_conversation(self, conversation_instance):
        self.conversation = conversation_instance

conversation_manager = ConversationManager()

# --- 2. Updated Prompt for a Stateful Agent ---
prompt = (
    "You are a friendly and efficient customer support agent for 'Aurora Commerce'. "
    "Your role is to assist users with returns and cancellations. "
    "When a user mentions they want to 'return' an item, your ONLY response must be to ask for their order number. "
    "After you ask for the order number, the system will process it. You will then receive a SYSTEM_MESSAGE with the result (SUCCESS or FAILURE). "
    "Based on that message, you must inform the user of the outcome. For example, if you get a success message, say 'Thank you. I have processed the return for your order.' "
    "If you get a failure message, relay that information politely, for example, 'I'm sorry, but I was unable to process the return for that order because it has already been cancelled.' "
    "Always be polite and conversational."
)
first_message = "Thank you for calling Aurora Commerce. How can I help you today?"

# --- Configuration for the Session ---
conversation_override = {"agent": {"prompt": {"prompt": prompt}, "first_message": first_message}}

# --- THIS IS THE CORRECTED LINE ---
# The ConversationConfig class in the latest library version is simpler.
# We no longer need to pass extra_body or dynamic_variables.
config = ConversationConfig(conversation_config_override=conversation_override)

client = ElevenLabs(api_key=API_KEY)

# --- Callback Functions ---
def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")

# --- 3. Updated Transcript Processor with State Logic ---
def process_user_transcript(transcript: str):
    print(f"User: {transcript}")
    
    current_state = conversation_manager.state
    transcript_lower = transcript.lower()

    if current_state == "AWAITING_ORDER_ID_FOR_RETURN":
        print(">>> SYSTEM: State is AWAITING_ORDER_ID. Attempting to extract order ID...")
        order_id = extract_order_id(transcript)

        if order_id:
            print(f">>> SYSTEM: Extracted Order ID: {order_id}. Processing return...")
            result_message = process_return_for_order(order_id)
            print(f">>> SYSTEM: Database result: {result_message}")
            
            if conversation_manager.conversation:
                conversation_manager.conversation.send_text(f"SYSTEM_MESSAGE: {result_message}")
            
            conversation_manager.state = "IDLE"
        else:
            print(">>> SYSTEM: No Order ID found in transcript. Letting agent re-prompt.")
            if conversation_manager.conversation:
                 conversation_manager.conversation.send_text("SYSTEM_MESSAGE: User did not provide a valid number. Please ask for the order number again politely.")

    elif "return" in transcript_lower:
        print(">>> SYSTEM: Keyword 'return' detected. Setting state to AWAITING_ORDER_ID_FOR_RETURN.")
        conversation_manager.state = "AWAITING_ORDER_ID_FOR_RETURN"

# --- Main Execution Block ---
try:
    print("Starting conversation... Press Ctrl+C to exit.")
    conversation = Conversation(
        client,
        AGENT_ID,
        config=config,
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=print_agent_response,
        callback_agent_response_correction=print_interrupted_response,
        callback_user_transcript=process_user_transcript,
    )

    conversation_manager.set_conversation(conversation)
    conversation.start_session()

except Exception as e:
    print(f"An error occurred: {e}")

