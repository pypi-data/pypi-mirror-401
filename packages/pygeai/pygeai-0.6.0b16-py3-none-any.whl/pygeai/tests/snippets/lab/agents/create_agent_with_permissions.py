from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Agent, AgentData, Prompt, LlmConfig, Model, Permission

# Create an agent with permissions configured
agent = Agent(
    name="Agent_With_Permissions",
    description="Agent demonstrating permissions configuration",
    access_scope="private",
    is_draft=True,
    sharing_scope="organization",
    permissions=Permission(
        allow_chat_sharing=True,
        allow_external_execution=False
    ),
    agent_data=AgentData(
        prompt=Prompt(
            instructions="You are a collaborative assistant that can be shared within the organization",
            inputs=["user_query"]
        ),
        llm_config=LlmConfig(max_tokens=2000),
        strategy_name="Dynamic Prompting",
        models=[Model(name="gpt-4-turbo-preview")]
    )
)

manager = AILabManager()
result = manager.create_agent(agent=agent, automatic_publish=False)

print(f"Created agent: {result.name}")
print(f"Agent ID: {result.id}")
print(f"Sharing scope: {result.sharing_scope}")
if result.permissions:
    print(f"\nPermissions:")
    print(f"  - Allow chat sharing: {result.permissions.allow_chat_sharing}")
    print(f"  - Allow external execution: {result.permissions.allow_external_execution}")
if result.effective_permissions:
    print(f"\nEffective Permissions:")
    print(f"  - Allow chat sharing: {result.effective_permissions.allow_chat_sharing}")
    print(f"  - Allow external execution: {result.effective_permissions.allow_external_execution}")
