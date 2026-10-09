SELECT
  CASE
    WHEN prev_leg_arr_delay IS NULL THEN '1. No prior leg that day'
    WHEN prev_leg_arr_delay <= 0    THEN '2. Prior leg early or on time'
    WHEN prev_leg_arr_delay <= 15   THEN '3. Prior leg 1-15 min late'
    WHEN prev_leg_arr_delay <= 60   THEN '4. Prior leg 16-60 min late'
    ELSE                                 '5. Prior leg 60+ min late'
  END AS prior_leg_status,
  COUNT(*)                      AS flights,
  ROUND(AVG(DepDel15) * 100, 1) AS pct_delayed_15min
FROM `airline-disruption-sql.airline.v_chain_delay`
GROUP BY prior_leg_status
ORDER BY prior_leg_status;
