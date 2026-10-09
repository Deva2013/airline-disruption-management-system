CREATE OR REPLACE VIEW `airline-disruption-sql.airline.v_flights_weather` AS
SELECT
  f.*,
  w.TempC,
  w.WindSpeedKt,
  w.WindGustKt,
  w.VisibSM,
  w.IsLowVis,
  w.IsHighWind,
  w.IsGust,
  w.FlightCategory,
  w.IsFogOrIFR,
  w.IATA IS NOT NULL AS has_weather
FROM `airline-disruption-sql.airline.v_hub_departures` AS f
LEFT JOIN `airline-disruption-sql.airline.weather` AS w
  ON  w.IATA    = f.Origin
  AND w.Date    = f.flight_date
  AND w.DepHour = f.ScheduledDepHour;
