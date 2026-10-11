select
    city,
    date_trunc(weather_date, month) as month,
    round(avg(temp_max_c), 1) as avg_max_temp_c,
    round(avg(temp_min_c), 1) as avg_min_temp_c,
    round(sum(precip_mm), 1) as total_precip_mm
from {{ ref('stg_weather') }}
group by 1, 2