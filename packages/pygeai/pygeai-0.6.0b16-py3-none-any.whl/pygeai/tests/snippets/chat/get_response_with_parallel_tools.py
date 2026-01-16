from pygeai.chat.clients import ChatClient

# Example: Using get_response with parallel tool calls
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = "What's the weather in New York and what time is it in Tokyo?"

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Enable parallel tool calls to execute both tools simultaneously
response = client.get_response(
    model=model,
    input=input_text,
    tools=tools,
    parallel_tool_calls=True,  # Allow multiple tools to be called in parallel
    temperature=0.7,
    max_output_tokens=1000
)

print("Response with parallel tool calls:")
print(response)
