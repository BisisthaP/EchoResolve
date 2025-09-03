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

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
# Make sure you have a .env file in the same directory with these variables
AGENT_ID = os.getenv("ELEVEN_AGENT_ID")
API_KEY = os.getenv("ELEVEN_API_KEY")

# Check if the environment variables are loaded correctly
if not AGENT_ID or not API_KEY:
    raise ValueError("ELEVEN_AGENT_ID and ELEVEN_API_KEY must be set in your .env file.")

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# --- 1. Updated Prompt for a Customer Support Agent ---
# This prompt defines the agent's role, capabilities, and personality.
prompt = (
    "You are a friendly, patient, and professional customer support agent for a company named 'Aurora Commerce'. "
    "Your primary role is to assist users with two specific tasks: processing returns and handling order cancellations. "
    "When a user asks for help, greet them warmly and ask how you can assist. "
    "If they mention 'return' or 'cancellation', guide them through the necessary steps. "
    "For returns, you will need to ask for their order number to begin the process. "
    "For cancellations, you will also ask for the order number to check the order's status. "
    "Remain focused on these tasks. If the user asks something outside of this scope, politely state that you can only help with returns and cancellations."
)

# The first message the agent will speak to the user.
first_message = "Thank you for calling Aurora Commerce. How can I help you today?"

# --- Configuration Overrides for the Session ---
conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=API_KEY)

# --- Callback Functions ---

def print_agent_response(response):
    """Prints the agent's full text response."""
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    """Handles cases where the agent is interrupted."""
    print(f"Agent interrupted, truncated response: {corrected}")

# --- 2. Function to Capture and Analyze the User Transcript ---
def process_user_transcript(transcript):
    """
    This function is called every time the user finishes speaking.
    It prints the transcript and checks for keywords.
    """
    print(f"User: {transcript}")
    
    # Check for the keyword "return" in the user's speech (case-insensitive)
    if "return" in transcript.lower():
        # This is where you would trigger your custom function for handling returns
        print("\n>>> SYSTEM: Keyword 'return' detected. Initiating return process logic... <<<\n")
    
    # You can add more keyword checks here
    if "cancel" in transcript.lower():
        print("\n>>> SYSTEM: Keyword 'cancel' detected. Initiating cancellation process logic... <<<\n")


# --- Initialize and Start the Conversation ---
# This single, correct initialization sets up the conversation with all callbacks.
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
        callback_user_transcript=process_user_transcript, # Use our new function here
    )

    # Start the conversation session. This will begin listening to the microphone.
    conversation.start_session()

except Exception as e:
    print(f"An error occurred: {e}")
