from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_total_tokens(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print(f"Total input tokens: {response.totalInputTokens}")
print(f"Total output tokens: {response.totalOutputTokens}")
print(f"Total tokens: {response.totalTokens}")
