import os
import zipfile
import requests
import pandas as pd
from datetime import datetime

URL = "https://peatus.ee/gtfs/gtfs.zip"
ZIPFILE = "bus_data.zip"
DATA_FOLDER_PATH = "bus_data"
STOPS_PATH = DATA_FOLDER_PATH + "/stops.txt"
STOP_TIMES_PATH = DATA_FOLDER_PATH + "/stop_times.txt"
TRIPS_PATH = DATA_FOLDER_PATH + "/trips.txt"
ROUTES_PATH = DATA_FOLDER_PATH + "/routes.txt"

def download_and_extract_gtfs():
    if not os.path.exists(ZIPFILE):
        print("Downloading GTFS data...")
        r = requests.get(URL)
        with open(ZIPFILE, "wb") as f:
            f.write(r.content)

    with zipfile.ZipFile(ZIPFILE, "r") as zip_ref:
        zip_ref.extractall(DATA_FOLDER_PATH)
    print("GTFS data downloaded and extracted.")

def load_line8_zoo_to_toompark_schedule():
    download_and_extract_gtfs()

    stops = pd.read_csv(STOPS_PATH)
    trips = pd.read_csv(TRIPS_PATH)
    stop_times = pd.read_csv(STOP_TIMES_PATH)
    routes = pd.read_csv(ROUTES_PATH)
    calendar = pd.read_csv(CALENDAR_PATH)

    # 🎯 Filter for weekday-only service_ids
    weekday_services = calendar[
        (calendar["monday"] == 1) &
        (calendar["tuesday"] == 1) &
        (calendar["wednesday"] == 1) &
        (calendar["thursday"] == 1) &
        (calendar["friday"] == 1) &
        (calendar["saturday"] == 0) &
        (calendar["sunday"] == 0)
    ]["service_id"].tolist()

    # 🔍 Filter route line 8
    route_8 = routes[routes["route_short_name"] == "8"]
    if route_8.empty:
        raise ValueError("Line 8 not found in GTFS data.")
    route_id = route_8.iloc[0]["route_id"]

    # 🎫 Filter trips that match route 8 and weekday services
    trips_8 = trips[
        (trips["route_id"] == route_id) &
        (trips["service_id"].isin(weekday_services))
    ]

    # 🚌 Join trips with stop_times
    merged = stop_times.merge(trips_8, on="trip_id")

    # 🔍 Get stop_ids for Zoo and Toompark
    zoo_stop = stops[stops["stop_name"].str.contains("Zoo", case=False, na=False)]
    toompark_stop = stops[stops["stop_name"].str.contains("Toompark", case=False, na=False)]
    if zoo_stop.empty or toompark_stop.empty:
        raise ValueError("Could not find Zoo or Toompark stops.")

    zoo_id = zoo_stop.iloc[0]["stop_id"]
    toompark_id = toompark_stop.iloc[0]["stop_id"]

    # ✅ Keep trips that go from Zoo → Toompark in correct order
    trips_with_both = merged[merged["stop_id"].isin([zoo_id, toompark_id])]
    grouped = trips_with_both.groupby("trip_id")

    valid_trip_ids = []
    for trip_id, group in grouped:
        stops_in_trip = group.sort_values("stop_sequence")
        stop_ids = stops_in_trip["stop_id"].tolist()
        if zoo_id in stop_ids and toompark_id in stop_ids:
            if stop_ids.index(zoo_id) < stop_ids.index(toompark_id):
                valid_trip_ids.append(trip_id)

    # 🕒 Get Zoo departure times for valid trips
    zoo_departures = merged[
        (merged["trip_id"].isin(valid_trip_ids)) &
        (merged["stop_id"] == zoo_id)
    ]

    # ⏱️ Keep times between 08:00–09:00
    times = []
    for t in zoo_departures["departure_time"]:
        try:
            time_obj = datetime.strptime(t, "%H:%M:%S")
            if time_obj.time() >= datetime.strptime("08:00", "%H:%M").time() and \
               time_obj.time() <= datetime.strptime("09:00", "%H:%M").time():
                times.append(time_obj)
        except:
            continue

    return sorted(times)
