SELECT
  hub,
  flight_date AS week_ending,
  pct_delayed_rolling_7d
FROM `airline-disruption-sql.airline.v_daily_hub_kpis`
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY hub
  ORDER BY pct_delayed_rolling_7d DESC
) = 1
ORDER BY pct_delayed_rolling_7d DESC;
