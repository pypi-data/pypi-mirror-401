from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Agent, AgentData, Prompt, LlmConfig, Model, Property

# Create an agent with properties
agent = Agent(
    name="Agent_With_Properties",
    description="Agent demonstrating the properties field",
    access_scope="private",
    is_draft=True,
    agent_data=AgentData(
        prompt=Prompt(
            instructions="You are a helpful assistant with custom properties",
            inputs=["user_query"]
        ),
        llm_config=LlmConfig(max_tokens=2000),
        strategy_name="Dynamic Prompting",
        models=[Model(name="gpt-4-turbo-preview")],
        properties=[
            Property(
                data_type="string",
                key="environment",
                value="production"
            ),
            Property(
                data_type="number",
                key="max_retries",
                value="3"
            ),
            Property(
                data_type="boolean",
                key="enable_logging",
                value="true"
            )
        ]
    )
)

manager = AILabManager()
result = manager.create_agent(agent=agent, automatic_publish=False)

print(f"Created agent with {len(result.agent_data.properties) if result.agent_data and result.agent_data.properties else 0} properties")
print(f"Agent ID: {result.id}")
if result.agent_data and result.agent_data.properties:
    print("\nProperties:")
    for prop in result.agent_data.properties:
        print(f"  - {prop.key} ({prop.data_type}): {prop.value}")
