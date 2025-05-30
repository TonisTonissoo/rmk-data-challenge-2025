from datetime import datetime, timedelta
import pandas as pd
from src.simulate import generate_bus_schedule, calculate_late_probability

def main():
    # 1. Generate bus schedule from 08:00 to 09:00, with 10 min intervals and up to ±60 sec jitter
    bus_schedule = generate_bus_schedule(
        start_time_str="08:00",
        end_time_str="09:00",
        interval_minutes=10,
        jitter_seconds=60
    )

    # 2. Prepare range of home departure times: every minute from 08:00 to 08:45
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("08:45", "%H:%M")
    departure_times = []
    current = start_time

    while current <= end_time:
        departure_times.append(current.strftime("%H:%M"))
        current += timedelta(minutes=1)

    # 3. Run simulations for each departure time
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

    # 4. Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("data/processed/late_probabilities.csv", index=False)
    print("\nResults saved to data/processed/late_probabilities.csv.")

if __name__ == "__main__":
    main()
