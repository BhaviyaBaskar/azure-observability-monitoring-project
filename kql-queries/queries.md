# KQL Queries

This file contains all the KQL queries used for monitoring, dashboards, and alerts.

--------------------------------------------------

ALERT QUERIES

High Error Rate Alert

CustomAppLogs_CL
| summarize 
    Total = count(), 
    Errors = countif(Status_s == "Error") 
    by bin(TimeGenerated, 5m)
| extend ErrorRate = round((Errors * 100.0) / Total, 2)
| where ErrorRate > 5


High Latency Alert

CustomAppLogs_CL
| summarize AvgResponseTime = round(avg(ResponseTime_d), 2) by bin(TimeGenerated, 5m)
| where AvgResponseTime > 500


--------------------------------------------------

DASHBOARD QUERIES

Total Requests

CustomAppLogs_CL
| summarize TotalRequests = count() by bin(TimeGenerated, 1m)
| project TimeGenerated, TotalRequests


Error Rate Trend

CustomAppLogs_CL
| summarize 
    Total = count(), 
    Errors = countif(Status_s == "Error") 
    by bin(TimeGenerated, 1m)
| extend ErrorRate = (Errors * 100.0) / Total


Average Response Time (Latency)

CustomAppLogs_CL
| summarize AvgResponseTime = avg(ResponseTime_d) by bin(TimeGenerated, 1m)


--------------------------------------------------

NOTES

- Alerts use 5-minute time window
- Dashboards use 1-minute time window
- Data is generated using Python script
- Metrics monitored:
  - Error Rate (%)
  - Response Time (ms)
  - Request Count

--------------------------------------------------

PURPOSE

These queries are used to:
- Monitor system health
- Track performance
- Trigger alerts for issues
- Visualize data in dashboards