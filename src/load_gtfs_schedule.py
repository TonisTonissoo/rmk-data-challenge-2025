import os
import zipfile
import requests
import pandas as pd
from datetime import datetime

# Config paths and URL
URL = "https://peatus.ee/gtfs/gtfs.zip"
ZIPFILE = "bus_data.zip"
DATA_FOLDER_PATH = "bus_data"
STOPS_PATH = os.path.join(DATA_FOLDER_PATH, "stops.txt")
STOP_TIMES_PATH = os.path.join(DATA_FOLDER_PATH, "stop_times.txt")
TRIPS_PATH = os.path.join(DATA_FOLDER_PATH, "trips.txt")
ROUTES_PATH = os.path.join(DATA_FOLDER_PATH, "routes.txt")
CALENDAR_PATH = os.path.join(DATA_FOLDER_PATH, "calendar.txt")

def download_and_extract_gtfs():
    """
    Downloads and extracts the GTFS (General Transit Feed Specification) data
    from the specified URL if not already downloaded.

    Creates a zip file locally and extracts its contents into the 'bus_data' folder.
    """
    if not os.path.exists(ZIPFILE):
        print("Downloading GTFS data...")
        r = requests.get(URL)
        with open(ZIPFILE, "wb") as f:
            f.write(r.content)

    with zipfile.ZipFile(ZIPFILE, "r") as zip_ref:
        zip_ref.extractall(DATA_FOLDER_PATH)
    print("GTFS data downloaded and extracted.")

def load_line8_zoo_to_toompark_schedule():
    """
    Loads and filters GTFS data for weekday trips on Tallinn's bus line 8
    from Zoo to Toompark.

    Returns:
        list of tuple: A list of (departure_time, arrival_time) pairs as datetime.time
                       objects for trips that go from Zoo to Toompark in correct order
                       and depart between 07:00 and 09:00.
    """
    # Load GTFS files
    stops = pd.read_csv(STOPS_PATH)
    stop_times = pd.read_csv(STOP_TIMES_PATH)
    trips = pd.read_csv(TRIPS_PATH)
    routes = pd.read_csv(ROUTES_PATH)
    calendar = pd.read_csv(CALENDAR_PATH)

    # Filter for weekday services
    weekday_services = calendar[
        (calendar["monday"] == 1) &
        (calendar["tuesday"] == 1) &
        (calendar["wednesday"] == 1) &
        (calendar["thursday"] == 1) &
        (calendar["friday"] == 1) &
        (calendar["saturday"] == 0) &
        (calendar["sunday"] == 0)
    ]["service_id"].tolist()

    # Get all route_ids for short name 8
    route_8 = routes[routes["route_short_name"] == "8"]
    if route_8.empty:
        print("Route 8 not found.")
        return []

    print(f"Found {len(route_8)} route(s) for line 8")

    # Filter all matching trips for any of these route_ids
    trips_8 = trips[
        (trips["route_id"].isin(route_8["route_id"])) &
        (trips["service_id"].isin(weekday_services))
    ]

    if trips_8.empty:
        print("No weekday trips found for route 8.")
        return []

    # Merge stop_times with trips
    merged = stop_times.merge(trips_8, on="trip_id")

    # Find all Zoo and Toompark stop_ids
    zoo_ids = stops[stops["stop_name"].str.contains("Zoo", case=False, na=False)]["stop_id"].unique().tolist()
    toompark_ids = stops[stops["stop_name"].str.contains("Toompark", case=False, na=False)]["stop_id"].unique().tolist()

    print(f"Zoo stop_ids: {zoo_ids}")
    print(f"Toompark stop_ids: {toompark_ids}")

    # Go through all trips and find those with both Zoo and Toompark in correct order
    result = []
    for trip_id, group in merged.groupby("trip_id"):
        group_sorted = group.sort_values("stop_sequence")
        stop_ids = group_sorted["stop_id"].tolist()

        zoo_index = next((i for i, sid in enumerate(stop_ids) if sid in zoo_ids), None)
        toompark_index = next((i for i, sid in enumerate(stop_ids) if sid in toompark_ids), None)

        if zoo_index is not None and toompark_index is not None and zoo_index < toompark_index:
            try:
                zoo_row = group_sorted.iloc[zoo_index]
                toompark_row = group_sorted.iloc[toompark_index]

                dep_time = pd.to_datetime(zoo_row["departure_time"], format="%H:%M:%S").time()
                arr_time = pd.to_datetime(toompark_row["arrival_time"], format="%H:%M:%S").time()
                result.append((dep_time, arr_time))
            except Exception:
                continue

    # Filter trips by departure time (e.g. 07:00 to 09:00)
    morning_start = datetime.strptime("07:00", "%H:%M").time()
    morning_end = datetime.strptime("09:00", "%H:%M").time()
    result = [pair for pair in result if morning_start <= pair[0] <= morning_end]

    print(f"Found {len(result)} valid Zoo → Toompark trips between 07:00 and 09:00.")
    return sorted(result)
