-- Check 1: hub departures view (expect 5,896,606 flights, 10 hubs, 2022-01-01 to 2024-12-31)
SELECT
  COUNT(*)               AS total_flights,
  COUNT(DISTINCT Origin) AS hubs,
  MIN(flight_date)       AS first_date,
  MAX(flight_date)       AS last_date,
  ROUND(AVG(DepDel15) * 100, 1) AS pct_delayed_15min
FROM `airline-disruption-sql.airline.v_hub_departures`;

-- Check 2: flights-to-weather join (expect 5,896,606 flights, 5,896,424 matched, ~100%)
SELECT
  COUNT(*)                                        AS total_flights,
  COUNTIF(has_weather)                            AS matched,
  ROUND(COUNTIF(has_weather) / COUNT(*) * 100, 2) AS pct_matched
FROM `airline-disruption-sql.airline.v_flights_weather`;
