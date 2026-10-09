CREATE OR REPLACE VIEW `airline-disruption-sql.airline.v_daily_hub_kpis` AS
WITH daily AS (
  SELECT
    flight_date,
    Origin           AS hub,
    COUNT(*)         AS flights,
    COUNT(DepDel15)  AS flights_operated,
    SUM(DepDel15)    AS delayed_flights,
    SUM(Cancelled)   AS cancelled_flights
  FROM `airline-disruption-sql.airline.v_hub_departures`
  GROUP BY flight_date, hub
)
SELECT
  *,
  ROUND(delayed_flights / flights_operated * 100, 1) AS pct_delayed_daily,
  ROUND(
    SUM(delayed_flights)  OVER w
    / SUM(flights_operated) OVER w * 100, 1
  ) AS pct_delayed_rolling_7d
FROM daily
WINDOW w AS (
  PARTITION BY hub
  ORDER BY flight_date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
);
