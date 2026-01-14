from pygeai.chat.clients import ChatClient

# Example: Using get_response with custom instructions
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = "Tell me about machine learning"

# Using instructions to customize the model's behavior
response = client.get_response(
    model=model,
    input=input_text,
    instructions="You are an expert educator who explains complex topics in simple terms suitable for beginners. Always use analogies and examples.",
    temperature=0.8,
    max_output_tokens=1500
)

print("Response with custom instructions:")
print(response)
