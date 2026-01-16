from pygeai.chat.clients import ChatClient

# Example: Using get_response with reasoning parameter
client = ChatClient()

model = "openai/o1-preview"
input_text = "Explain the concept of quantum entanglement in simple terms"

# Using reasoning parameter to control reasoning effort
response = client.get_response(
    model=model,
    input=input_text,
    reasoning={
        "type": "default",  # Can be "default", "high", "medium", "low"
        "effort": "medium"
    },
    max_output_tokens=2000
)

print("Response with reasoning:")
print(response)
