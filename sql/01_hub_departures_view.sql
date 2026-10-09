CREATE OR REPLACE VIEW `airline-disruption-sql.airline.v_hub_departures` AS
SELECT
  DATE(Year, Month, DayofMonth) AS flight_date,
  * EXCEPT (FlightDate)
FROM `airline-disruption-sql.airline.flights`
WHERE Origin IN ('JFK','ORD','ATL','LAX','DFW','SFO','EWR','MIA','SEA','BOS');
