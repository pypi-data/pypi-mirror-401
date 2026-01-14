from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_top_10_agents_by_requests(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print("Top 10 agents by requests:")
for idx, agent in enumerate(response.topAgents, 1):
    print(f"{idx}. {agent.agentName}: {agent.totalRequests} requests")
