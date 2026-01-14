from pygeai.chat.clients import ChatClient

# Example: Using get_response with truncation strategy
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = """
This is a very long input text that might exceed the context window.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod 
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
""" * 100  # Simulate long input

# Using truncation to handle long inputs
response = client.get_response(
    model=model,
    input=input_text,
    truncation="auto",  # Options: "auto", "disabled"
    max_output_tokens=1000,
    temperature=0.7
)

print("Response with truncation handling:")
print(response)
