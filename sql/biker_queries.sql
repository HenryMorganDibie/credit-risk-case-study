-- Query 1: Day of the week with the longest average trip
SELECT 
    TRIM(TO_CHAR(CAST(start_time AS TIMESTAMP), 'Day')) AS day_of_week, 
    AVG(duration_minutes) AS avg_duration
FROM biker_data
WHERE end_station_name NOT IN ('Missing', 'Stolen')
  AND start_station_name != end_station_name
GROUP BY 1
ORDER BY avg_duration DESC
LIMIT 1;

-- Query 2: Month/Year with the most bike trips
SELECT 
    TO_CHAR(CAST(start_time AS TIMESTAMP), 'YYYY-MM') AS month_year,
    COUNT(*) AS total_trips
FROM biker_data
GROUP BY 1
ORDER BY total_trips DESC
LIMIT 1;

-- Query 3: Longest and Shortest Duration
(SELECT 'Longest' as category, trip_id, duration_minutes, start_time 
 FROM biker_data 
 WHERE end_station_name NOT IN ('Missing', 'Stolen') AND start_station_name != end_station_name
 ORDER BY duration_minutes DESC, start_time ASC 
 LIMIT 1)
UNION ALL
(SELECT 'Shortest' as category, trip_id, duration_minutes, start_time 
 FROM biker_data 
 WHERE end_station_name NOT IN ('Missing', 'Stolen') AND start_station_name != end_station_name
 ORDER BY duration_minutes ASC, start_time ASC 
 LIMIT 1);