select
    city,
    date as weather_date,
    temp_max_c,
    temp_min_c,
    precip_mm
from {{ source('raw', 'weather_daily') }}
where true
qualify row_number() over (
    partition by city, date
    order by loaded_at desc
) = 1