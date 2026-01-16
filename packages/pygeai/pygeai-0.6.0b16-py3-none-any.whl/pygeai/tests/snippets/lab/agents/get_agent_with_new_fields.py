from pygeai.lab.managers import AILabManager

# Get an agent and inspect all new fields
manager = AILabManager()

# First, list agents to get an ID
agents = manager.get_agent_list()
if len(agents) == 0:
    print("No agents found. Please create an agent first.")
    exit(1)

# Get the first agent
agent_id = agents[0].id
agent = manager.get_agent(agent_id)

print(f"Agent: {agent.name} (ID: {agent.id})")
print(f"Status: {agent.status}")
print(f"Is Draft: {agent.is_draft}")
print(f"\n=== New Fields ===")

# Sharing scope
print(f"\nSharing Scope: {agent.sharing_scope}")

# Permissions
if agent.permissions:
    print(f"\nPermissions:")
    print(f"  - Allow chat sharing: {agent.permissions.allow_chat_sharing}")
    print(f"  - Allow external execution: {agent.permissions.allow_external_execution}")
else:
    print(f"\nPermissions: None")

# Effective permissions
if agent.effective_permissions:
    print(f"\nEffective Permissions:")
    print(f"  - Allow chat sharing: {agent.effective_permissions.allow_chat_sharing}")
    print(f"  - Allow external execution: {agent.effective_permissions.allow_external_execution}")
else:
    print(f"\nEffective Permissions: None")

# Agent data properties
if agent.agent_data:
    print(f"\nAgent Data:")
    print(f"  - Strategy Name: {agent.agent_data.strategy_name}")
    
    if agent.agent_data.properties:
        print(f"  - Properties ({len(agent.agent_data.properties)}):")
        for prop in agent.agent_data.properties:
            print(f"    * {prop.key} ({prop.data_type}): {prop.value}")
    else:
        print(f"  - Properties: None")
    
    if agent.agent_data.models:
        print(f"  - Models: {len(agent.agent_data.models)} configured")
    else:
        print(f"  - Models: None")
    
    if agent.agent_data.resource_pools:
        print(f"  - Resource Pools: {len(agent.agent_data.resource_pools)} configured")
    else:
        print(f"  - Resource Pools: None")
else:
    print(f"\nAgent Data: None")
