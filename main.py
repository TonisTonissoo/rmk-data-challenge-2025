from datetime import datetime, timedelta
import pandas as pd
from src.simulate import calculate_late_probability
from src.plot_results import plot_late_probabilities
from src.download_realtime import download_and_save_line8_realtime

def parse_departure_times_from_realtime(csv_path):
    """
    Extracts and parses bus departure times from real-time GPS data CSV.
    Assumes 'timestamp' column in ISO format.
    Returns a list of datetime objects.
    """
    df = pd.read_csv(csv_path)

    if "timestamp" not in df.columns:
        raise ValueError("CSV must contain a 'timestamp' column.")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Optional: filter for time window
    start_time = datetime.strptime("08:00", "%H:%M").time()
    end_time = datetime.strptime("09:00", "%H:%M").time()
    df_filtered = df[(df["timestamp"].dt.time >= start_time) & (df["timestamp"].dt.time <= end_time)]

    bus_times = sorted(df_filtered["timestamp"].tolist())
    return bus_times

def main():
    # 1. Download and save real-time data
    print("Fetching real-time data for bus line 8...")
    download_and_save_line8_realtime("data/raw/bus_line8_realtime.csv")

    # 2. Parse real departure times from saved file
    bus_schedule = parse_departure_times_from_realtime("data/raw/bus_line8_realtime.csv")
    print(f"Using {len(bus_schedule)} real departure times.")

    # 3. Create departure time range from 08:00 to 08:45
    departure_times = []
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("08:45", "%H:%M")
    current = start_time

    while current <= end_time:
        departure_times.append(current.strftime("%H:%M"))
        current += timedelta(minutes=1)

    # 4. Run lateness simulations
    results = []
    print("Running simulations...")
    for time_str in departure_times:
        probability = calculate_late_probability(
            departure_time_str=time_str,
            bus_schedule=bus_schedule,
            n_simulations=1000
        )
        results.append({
            "departure_time": time_str,
            "late_probability": probability
        })
        print(f"Departure {time_str} → Late probability: {probability:.2%}")

    # 5. Save results
    df = pd.DataFrame(results)
    df.to_csv("data/processed/late_probabilities.csv", index=False)
    print("\nResults saved to data/processed/late_probabilities.csv.")

    # 6. Plot
    plot_late_probabilities(
        "data/processed/late_probabilities.csv",
        save_path="data/processed/late_probability_plot.png"
    )

if __name__ == "__main__":
    main()
