from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_total_active_users(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print(f"Total active users: {response.totalActiveUsers}")
