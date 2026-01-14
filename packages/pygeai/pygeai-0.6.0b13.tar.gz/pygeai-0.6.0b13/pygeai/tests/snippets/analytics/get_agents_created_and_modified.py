from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_agents_created_and_modified(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print(f"Created agents: {response.createdAgents}")
print(f"Modified agents: {response.modifiedAgents}")
