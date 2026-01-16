from pygeai.chat.clients import ChatClient

# Example: Using get_response with metadata and user identification
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = "What are the benefits of using AI in healthcare?"

# Using metadata to pass additional context
response = client.get_response(
    model=model,
    input=input_text,
    metadata={
        "request_id": "req_12345",
        "department": "healthcare",
        "priority": "high"
    },
    user="user_jane_doe",  # User identifier for tracking
    temperature=0.7,
    max_output_tokens=1500
)

print("Response with metadata:")
print(response)
