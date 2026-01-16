from pygeai.chat.clients import ChatClient

# Example: Comprehensive usage of get_response with all major parameters
client = ChatClient()

model = "openai/gpt-4-turbo-preview"
input_text = "Analyze the benefits of renewable energy and suggest implementation strategies"

# Define a tool for additional data retrieval
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_energy_stats",
            "description": "Get statistics about renewable energy adoption",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Country name"
                    },
                    "year": {
                        "type": "integer",
                        "description": "Year for statistics"
                    }
                },
                "required": ["country"]
            }
        }
    }
]

# Comprehensive configuration
response = client.get_response(
    model=model,
    input=input_text,
    instructions="You are an energy policy expert. Provide detailed, data-driven analysis with actionable recommendations.",
    tools=tools,
    tool_choice="auto",  # Let the model decide when to use tools
    parallel_tool_calls=True,
    temperature=0.7,
    max_output_tokens=2000,
    top_p=0.9,
    metadata={
        "request_id": "energy_analysis_001",
        "department": "sustainability",
        "priority": "high"
    },
    user="analyst_john_doe",
    reasoning={
        "effort": "high"  # Request thorough reasoning
    },
    truncation="auto",
    store=True  # Store for future reference
)

print("=== Comprehensive Response ===")
print(response)

# Extract key information if response is a dict
if isinstance(response, dict):
    print("\n=== Response Metadata ===")
    if "usage" in response:
        print(f"Tokens used: {response['usage']}")
    if "model" in response:
        print(f"Model used: {response['model']}")
