CREATE OR REPLACE VIEW `airline-disruption-sql.airline.v_chain_delay` AS
WITH legs AS (
  SELECT
    DATE(Year, Month, DayofMonth) AS flight_date,
    * EXCEPT (FlightDate)
  FROM `airline-disruption-sql.airline.flights`
  WHERE Tail_Number IS NOT NULL
    AND Tail_Number != ''
),
sequenced AS (
  SELECT
    *,
    LAG(Dest)     OVER w AS prev_dest,
    LAG(ArrDelay) OVER w AS prev_arr_delay
  FROM legs
  WINDOW w AS (
    PARTITION BY Tail_Number, flight_date
    ORDER BY CRSDepTime, FlightNumber
  )
)
SELECT
  * EXCEPT (prev_dest, prev_arr_delay),
  IF(prev_dest = Origin, prev_arr_delay, NULL) AS prev_leg_arr_delay
FROM sequenced
WHERE Origin IN ('JFK','ORD','ATL','LAX','DFW','SFO','EWR','MIA','SEA','BOS');
