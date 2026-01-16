from pygeai.chat.clients import ChatClient

# Example: Using get_response with store parameter to persist conversation
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = "Remember that my favorite color is blue. What did I just tell you?"

# Use store parameter to enable conversation storage
response = client.get_response(
    model=model,
    input=input_text,
    store=True,  # Store this conversation for future reference
    user="user_123",  # Associate with specific user
    metadata={
        "session_id": "session_abc",
        "conversation_type": "preference_learning"
    },
    temperature=0.7,
    max_output_tokens=500
)

print("Response with conversation storage:")
print(response)

# Follow-up request can reference stored context
follow_up = client.get_response(
    model=model,
    input="What's my favorite color?",
    store=True,
    user="user_123",
    metadata={
        "session_id": "session_abc"
    }
)

print("\nFollow-up response:")
print(follow_up)
