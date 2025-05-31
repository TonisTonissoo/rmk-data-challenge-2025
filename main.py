from datetime import datetime, timedelta
import pandas as pd
from src.simulate import calculate_late_probability
from src.plot_results import plot_late_probabilities
from src.load_gtfs_schedule import load_line8_zoo_to_toompark_schedule

def main():
    # 1. Load real bus schedule from GTFS (Zoo → Toompark, line 8)
    print("Loading GTFS schedule for bus line 8 Zoo → Toompark...")
    bus_schedule = load_line8_zoo_to_toompark_schedule()
    print(f"Using {len(bus_schedule)} GTFS-based departure times.")

    # 2. Create departure time range from 08:00 to 08:45
    departure_times = []
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("08:45", "%H:%M")
    current = start_time

    while current <= end_time:
        departure_times.append(current.strftime("%H:%M"))
        current += timedelta(minutes=1)

    # 3. Run lateness simulations
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

    # 4. Save results
    df = pd.DataFrame(results)
    df.to_csv("data/processed/late_probabilities.csv", index=False)
    print("\nResults saved to data/processed/late_probabilities.csv.")

    # 5. Plot results
    plot_late_probabilities(
        "data/processed/late_probabilities.csv",
        save_path="data/processed/late_probability_plot.png"
    )

if __name__ == "__main__":
    main()
