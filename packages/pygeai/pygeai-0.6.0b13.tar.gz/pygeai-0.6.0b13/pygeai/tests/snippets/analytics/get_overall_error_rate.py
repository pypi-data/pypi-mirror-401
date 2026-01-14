from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_overall_error_rate(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print(f"Overall error rate: {response.errorRate:.2%}")
