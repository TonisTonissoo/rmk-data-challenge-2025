import pandas as pd

# GTFS failide teed
STOPS = "bus_data/stops.txt"
STOP_TIMES = "bus_data/stop_times.txt"
TRIPS = "bus_data/trips.txt"

# Lae andmed
stops = pd.read_csv(STOPS)
stop_times = pd.read_csv(STOP_TIMES)
trips = pd.read_csv(TRIPS)

# Otsi Zoo ja Toompark stop_id-d
zoo_ids = stops[stops["stop_name"].str.contains("Zoo", case=False)]["stop_id"].unique()
toompark_ids = stops[stops["stop_name"].str.contains("Toompark", case=False)]["stop_id"].unique()

print("Zoo stop_ids:", zoo_ids)
print("Toompark stop_ids:", toompark_ids)

# Leia trip_id-d, kus on mõlemad
zoo_trips = stop_times[stop_times["stop_id"].isin(zoo_ids)]["trip_id"].unique()
toompark_trips = stop_times[stop_times["stop_id"].isin(toompark_ids)]["trip_id"].unique()

common_trips = set(zoo_trips).intersection(set(toompark_trips))
print(f"\nLeitud ühiseid trip_id-sid: {len(common_trips)}")

# Vali üks näidistrip ja näita selle peatusi
if common_trips:
    example_trip_id = list(common_trips)[0]
    print(f"\nNäidis trip_id: {example_trip_id}")
    sequence = stop_times[stop_times["trip_id"] == example_trip_id].sort_values("stop_sequence")
    sequence = sequence.merge(stops[["stop_id", "stop_name"]], on="stop_id", how="left")
    print(sequence[["stop_sequence", "stop_name", "departure_time"]])
else:
    print("\nEi leitud ühtegi reisi, kus oleks Zoo → Toompark.")
