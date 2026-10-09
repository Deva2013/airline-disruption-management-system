WITH carrier_hub AS (
  SELECT
    Origin                        AS hub,
    Airline,
    COUNT(*)                      AS flights,
    ROUND(AVG(DepDel15) * 100, 1) AS pct_delayed_15min
  FROM `airline-disruption-sql.airline.v_hub_departures`
  GROUP BY hub, Airline
  HAVING COUNT(*) >= 10000
)
SELECT
  hub,
  Airline,
  flights,
  pct_delayed_15min,
  RANK() OVER (
    PARTITION BY hub
    ORDER BY pct_delayed_15min DESC
  ) AS delay_rank
FROM carrier_hub
QUALIFY delay_rank <= 3
ORDER BY hub, delay_rank;
