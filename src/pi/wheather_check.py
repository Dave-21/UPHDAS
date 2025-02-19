"""
Make decision on whether to run the unit or not

    - Loads config file from config.yaml
    - Determines astronomical twilight period (pitch black hours) - With skyfield
    - Gets hourly NWS (NOAA) forecasts during dark period for cloud cover, rain, and snow precipitation
    - Calculates Moon phase at midpoint of running hours - With skyfield
    - Makes a decision on whether to run the unit based on thresholds in config file
        (cloud coverage, moon illumination, rain probability, and snow probabilty)
    - If debug mode is enabled, the hourly forecast is printed
    - If the decision is to run the unit, the astronomical dark time period is outputted

Decision logic:
    The unit runs if:
        - Average cloud coverage is below the threshold.
        - Moon illumination is below the threshold.
        - The maximum hourly rain probability is below rain_threshold (or rain is allowed).
        - The maximum hourly snow probability is below snow_threshold (or snow is allowed).
"""

import os
import requests
import argparse
import yaml
from datetime import datetime, timedelta, timezone
from dateutil import parser as dt_parser
from zoneinfo import ZoneInfo

# Skyfield imports
from skyfield.api import load, wgs84
from skyfield import almanac
from skyfield.framelib import ecliptic_frame

def load_config(config_file="config.yaml"):
    if not os.path.exists(config_file):
        print("Config file not found, using defaults.")
        return {}
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config.get("pi_config", {})

# Short forecast
def forecast_to_cloud_cover(description):
    desc = description.lower()
    if "mostly clear" in desc or "mostly sunny" in desc:
        return 10
    elif "clear" in desc or "sunny" in desc:
        return 0
    elif "partly cloudy" in desc:
        return 50
    elif "partly sunny" in desc:
        return 40
    elif "mostly cloudy" in desc:
        return 80
    elif "cloudy" in desc or "overcast" in desc:
        return 100
    else:
        return 50

# Get hourly forecast data from NWS API for location in config file and time window
# Cloud coverage, precipitation probabilty for rain and snow
# Returns list of tuples: 
#   [forecast_time (UTC), cloud_coverage_percentage, shortForecast, rain_probability, snow_probabilty]
def get_nws_hourly_forecasts(lat, lon, start_dt, end_dt):
    headers = {"User-Agent": "MySatelliteProject/1.0 (contact@example.com)"}
    try:
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        r = requests.get(points_url, headers=headers, timeout=10)
        r.raise_for_status()
        points_data = r.json()
    except Exception as ex:
        print(f"Error retrieving points data: {ex}")
        return []
    
    forecast_hourly_url = points_data.get("properties", {}).get("forecastHourly")
    if not forecast_hourly_url:
        print("No hourly forecast URL found.")
        return []
    
    try:
        r = requests.get(forecast_hourly_url, headers=headers, timeout=10)
        r.raise_for_status()
        forecast_data = r.json()
    except Exception as ex:
        print(f"Error retrieving forecast data: {ex}")
        return []
    
    periods = forecast_data.get("properties", {}).get("periods", [])
    if not periods:
        print("No forecast periods found.")
        return []
    
    forecast_list = []
    for period in periods:
        start_time_str = period.get("startTime")
        if not start_time_str:
            continue
        try:
            dt_obj = dt_parser.isoparse(start_time_str).astimezone(timezone.utc)
        except Exception:
            continue
        if start_dt <= dt_obj <= end_dt:
            cc = period.get("cloudCover")
            sf = period.get("shortForecast", "")
            if cc is None:
                cc = forecast_to_cloud_cover(sf)
            # Attempt to get precipitation probability
            precip_val = 0
            if "probabilityOfPrecipitation" in period:
                try:
                    precip = period["probabilityOfPrecipitation"]
                    if precip and precip.get("value") is not None:
                        precip_val = precip.get("value")
                except Exception:
                    precip_val = 0
            # Determine rain vs. snow from forecast text:
            ft_lower = sf.lower()
            if "rain" in ft_lower and "snow" not in ft_lower:
                rain_prob = precip_val
                snow_prob = 0
            elif "snow" in ft_lower and "rain" not in ft_lower:
                snow_prob = precip_val
                rain_prob = 0
            elif "rain" in ft_lower and "snow" in ft_lower:
                # Mixed; assign half of the probability to each
                rain_prob = precip_val / 2
                snow_prob = precip_val / 2
            else:
                rain_prob = 0
                snow_prob = 0
            
            forecast_list.append((dt_obj, cc, sf, rain_prob, snow_prob))
    return forecast_list

# Determines astronomical dark period for night at the given location using skyfield
# Returns tuple: (dark_start, dark_end) as UTC datetime objects
def get_dark_period(lat, lon, tz_name="America/Detroit"):
    ts = load.timescale()
    eph = load('de421.bsp')
    
    local_tz = ZoneInfo(tz_name)
    now_local = datetime.now(local_tz)
    #today = now_local.date()
    yesterday = now_local.date()
    today = yesterday + timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    # Define interval: 18:00 today to 06:00 tomorrow
    start_local = datetime.combine(today, datetime.min.time(), tzinfo=local_tz).replace(hour=18)
    end_local = datetime.combine(tomorrow, datetime.min.time(), tzinfo=local_tz).replace(hour=6)
    
    t0 = ts.from_datetime(start_local)
    t1 = ts.from_datetime(end_local)
    
    observer = wgs84.latlon(lat, lon)
    f = almanac.dark_twilight_day(eph, observer)
    times, states = almanac.find_discrete(t0, t1, f)
    
    dark_start = None
    dark_end = None
    for t, state in zip(times, states):
        if dark_start is None and state == 0:
            dark_start = t
        elif dark_start is not None and state != 0:
            dark_end = t
            break

    if dark_start is None or dark_end is None:
        print("Could not determine dark period.")
        return None, None
    
    return dark_start.utc_datetime(), dark_end.utc_datetime()

# Calculates Moon phase given UTC datetime
# Returns a tuple: (phase_angle (deg), percent illuminated)
def get_moon_phase(dt_utc):
    ts = load.timescale()
    eph = load('de421.bsp')
    t = ts.from_datetime(dt_utc)
    
    sun = eph['sun']
    moon = eph['moon']
    earth = eph['earth']
    
    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()
    
    _, slon, _ = s.frame_latlon(ecliptic_frame)
    _, mlon, _ = m.frame_latlon(ecliptic_frame)
    phase_angle = (mlon.degrees - slon.degrees) % 360.0
    percent_illuminated = 100.0 * m.fraction_illuminated(sun)
    
    return phase_angle, percent_illuminated

# main
def main():
    parser_arg = argparse.ArgumentParser(
        description="Determine dark period, fetch NWS forecasts (clouds, rain, snow), compute moon phase, "
                    "and decide whether to run the unit."
    )
    # Default command-line arguments (overridden by config file)
    parser_arg.add_argument("--lat", type=float, default=46.4977, help="Latitude")
    parser_arg.add_argument("--lon", type=float, default=-84.3476, help="Longitude")
    parser_arg.add_argument("--cloud_threshold", type=float, default=50,
                            help="Max acceptable average cloud coverage percentage")
    parser_arg.add_argument("--moon_threshold", type=float, default=50,
                            help="Max acceptable moon illumination percentage")
    parser_arg.add_argument("--rain_threshold", type=float, default=20,
                            help="Max acceptable rain probability percentage")
    parser_arg.add_argument("--snow_threshold", type=float, default=20,
                            help="Max acceptable snow probability percentage")
    parser_arg.add_argument("--allow_rain", type=lambda x: (str(x).lower() == "true"), default=False,
                            help="Allow running when rain is forecast (default: False)")
    parser_arg.add_argument("--allow_snow", type=lambda x: (str(x).lower() == "true"), default=False,
                            help="Allow running when snow is forecast (default: False)")
    parser_arg.add_argument("--tz", type=str, default="America/Detroit", help="Local timezone")
    parser_arg.add_argument("--debug", type=lambda x: (str(x).lower() == "true"), default=True,
                            help="Enable debug output (default: True)")
    args = parser_arg.parse_args()
    
    # Load configuration from config.yaml and override defaults
    config = load_config()
    if config:
        args.lat = config.get("latitude", args.lat)
        args.lon = config.get("longitude", args.lon)
        args.cloud_threshold = config.get("cloud_threshold", args.cloud_threshold)
        args.moon_threshold = config.get("moon_threshold", args.moon_threshold)
        args.rain_threshold = config.get("rain_threshold", args.rain_threshold)
        args.snow_threshold = config.get("snow_threshold", args.snow_threshold)
        args.allow_rain = config.get("allow_rain", args.allow_rain)
        args.allow_snow = config.get("allow_snow", args.allow_snow)
        args.tz = config.get("timezone", args.tz)
        args.debug = config.get("debug", args.debug)
    
    if args.debug:
        print("Configuration:")
        print(f"  Location: {args.lat}, {args.lon}")
        print(f"  Cloud Threshold: {args.cloud_threshold}%")
        print(f"  Moon Threshold: {args.moon_threshold}%")
        print(f"  Rain Threshold: {args.rain_threshold}% (Allowed: {args.allow_rain})")
        print(f"  Snow Threshold: {args.snow_threshold}% (Allowed: {args.allow_snow})")
        print(f"  Timezone: {args.tz}")
        print(f"  Debug Mode: {args.debug}\n")
    
    # Determine the astronomically dark period
    dark_start, dark_end = get_dark_period(args.lat, args.lon, args.tz)
    if dark_start is None or dark_end is None:
        print("Failed to determine dark period.")
        return
    
    if args.debug:
        print("Dark period (UTC):")
        print(f"  Start: {dark_start.isoformat()}")
        print(f"  End:   {dark_end.isoformat()}\n")
    
    # Retrieve hourly forecasts during the dark period
    forecasts = get_nws_hourly_forecasts(args.lat, args.lon, dark_start, dark_end)
    if not forecasts:
        print("No forecast data available from NWS for the dark period.")
        return
    
    total_cloud = 0
    count = 0
    max_rain_prob = 0
    max_snow_prob = 0
    
    if args.debug:
        print("Hourly Forecasts during dark period:")
    for t, cc, sf, rain_prob, snow_prob in forecasts:
        if args.debug:
            print(f"  {t.isoformat()} : {cc}% clouds, Forecast: {sf}, "
                  f"Rain Prob: {rain_prob}%, Snow Prob: {snow_prob}%")
        total_cloud += cc
        count += 1
        max_rain_prob = max(max_rain_prob, rain_prob)
        max_snow_prob = max(max_snow_prob, snow_prob)
    
    avg_cloud = total_cloud / count if count > 0 else 100
    if args.debug:
        print(f"\nAverage Cloud Coverage: {avg_cloud:.1f}%")
        print(f"Maximum Rain Probability: {max_rain_prob}%")
        print(f"Maximum Snow Probability: {max_snow_prob}%\n")
    
    # Calculate moon phase at the midpoint of the dark period
    midpoint = dark_start + (dark_end - dark_start) / 2
    phase_angle, percent_illuminated = get_moon_phase(midpoint)
    if args.debug:
        print(f"Moon Phase at {midpoint.isoformat()} UTC:")
        print(f"  Phase Angle: {phase_angle:.1f}°")
        print(f"  Percent Illuminated: {percent_illuminated:.1f}%\n")
    
    if (avg_cloud < args.cloud_threshold and
        percent_illuminated < args.moon_threshold and
        (max_rain_prob < args.rain_threshold or args.allow_rain) and
        (max_snow_prob < args.snow_threshold or args.allow_snow)):
        decision = "Run the unit."
    else:
        decision = "Do NOT run the unit."
    
    print("Decision: " + decision)
    
    # Output pitch balck hours (astronomical period) if decision is run
    if decision == "Run the unit.":
        local_tz = ZoneInfo(args.tz)
        dark_start_local = dark_start.astimezone(local_tz)
        dark_end_local = dark_end.astimezone(local_tz)
        print("\nRun the unit during the pitch black (astronomical dark) hours:")
        print(f"  Start (Local): {dark_start_local.isoformat()}")
        print(f"  End (Local):   {dark_end_local.isoformat()}")

if __name__ == "__main__":
    main()
