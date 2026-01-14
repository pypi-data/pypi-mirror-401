from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_average_cost_per_request(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print(f"Average cost per request: ${response.averageCost:.4f}")
