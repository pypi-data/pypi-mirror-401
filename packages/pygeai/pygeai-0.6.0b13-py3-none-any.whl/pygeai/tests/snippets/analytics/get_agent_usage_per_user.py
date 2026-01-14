from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_agent_usage_per_user(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print("Agent usage per user:")
for user in response.agentUsagePerUser:
    print(f"User: {user.userName or user.userId}")
    print(f"  Requests: {user.totalRequests}")
    print(f"  Tokens: {user.totalTokens}")
    print(f"  Cost: ${user.totalCost:.2f}")
    print()
