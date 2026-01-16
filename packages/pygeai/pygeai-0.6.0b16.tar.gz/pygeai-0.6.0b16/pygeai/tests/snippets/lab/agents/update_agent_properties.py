from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Property

# Update an agent's properties
manager = AILabManager()

# Get an existing agent
agents = manager.get_agent_list()
if len(agents) == 0:
    print("No agents found. Please create an agent first.")
    exit(1)

agent = manager.get_agent(agents[0].id)
print(f"Updating agent: {agent.name}")

# Update agent data properties
if agent.agent_data:
    # Add or update properties
    agent.agent_data.properties = [
        Property(
            data_type="string",
            key="version",
            value="2.0.0"
        ),
        Property(
            data_type="string",
            key="region",
            value="us-east-1"
        ),
        Property(
            data_type="boolean",
            key="auto_scale",
            value="true"
        )
    ]
    
    # Update the agent
    updated_agent = manager.update_agent(agent)
    
    print(f"\nAgent updated successfully!")
    print(f"Agent ID: {updated_agent.id}")
    
    if updated_agent.agent_data and updated_agent.agent_data.properties:
        print(f"\nUpdated Properties ({len(updated_agent.agent_data.properties)}):")
        for prop in updated_agent.agent_data.properties:
            print(f"  - {prop.key} ({prop.data_type}): {prop.value}")
    else:
        print("\nNo properties found after update")
else:
    print("Agent has no agent_data, cannot update properties")
