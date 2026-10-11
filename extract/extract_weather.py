from datetime import datetime, timezone

import requests

URL = "https://archive-api.open-meteo.com/v1/archive"
CITIES = {
    "abu_dhabi": (24.4539, 54.3773),
    "dubai": (25.2048, 55.2708),
    "kochi": (9.9312, 76.2673),
    "bengaluru": (12.9716, 77.5946),
}


def fetch_city(city, lat, lon, start, end):
    resp = requests.get(
        URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto",
        },
        timeout=30,
    )
    resp.raise_for_status()
    d = resp.json()["daily"]
    loaded_at = datetime.now(timezone.utc).isoformat()
    return [
        {
            "city": city,
            "date": t,
            "temp_max_c": mx,
            "temp_min_c": mn,
            "precip_mm": p,
            "loaded_at": loaded_at,
        }
        for t, mx, mn, p in zip(
            d["time"],
            d["temperature_2m_max"],
            d["temperature_2m_min"],
            d["precipitation_sum"],
        )
    ]


def fetch_all(start, end):
    rows = []
    for city, (lat, lon) in CITIES.items():
        rows += fetch_city(city, lat, lon, start, end)
    return rows