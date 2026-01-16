from pygeai.analytics.managers import AnalyticsManager

manager = AnalyticsManager()

response = manager.get_total_requests_per_day(
    start_date="2025-01-01",
    end_date="2026-01-31"
)

print("Requests per day:")
for item in response.requestsPerDay:
    print(f"  Date: {item.date}, Total: {item.totalRequests}, Errors: {item.totalRequestsWithError}")
