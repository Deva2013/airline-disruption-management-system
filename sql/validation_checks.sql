-- Check 1: hub departures view (expect 5,896,606 flights, 10 hubs, 2022-01-01 to 2024-12-31)
SELECT
  COUNT(*)               AS total_flights,
  COUNT(DISTINCT Origin) AS hubs,
  MIN(flight_date)       AS first_date,
  MAX(flight_date)       AS last_date,
  ROUND(AVG(DepDel15) * 100, 1) AS pct_delayed_15min
FROM `airline-disruption-sql.airline.v_hub_departures`;
