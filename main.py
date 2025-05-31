from datetime import datetime
import pandas as pd
from src.simulate import calculate_late_probability
from src.plot_results import plot_late_probabilities
from src.load_gtfs_schedule import load_line8_zoo_to_toompark_schedule
import os

def main():
    """
    Main pipeline for computing and visualizing the probability of being late
    when departing from home to reach a 09:05 meeting using GTFS bus schedules.

    Steps:
        1. Load GTFS data for line 8 from Zoo to Toompark.
        2. Compute lateness probabilities based on walking and bus times.
        3. Save results to CSV.
        4. Print a summary of schedule entries.
        5. Generate and save a visual plot of lateness probabilities.

    Note:
        Walking times and meeting time are hardcoded. Assumes GTFS data is
        available or downloadable from peatus.ee.
    """
    # 1. Load bus schedule from GTFS (Zoo → Toompark, line 8)
    print("Loading GTFS schedule for bus line 8 Zoo → Toompark...")
    bus_schedule = load_line8_zoo_to_toompark_schedule()

    if not bus_schedule:
        print("No valid trips found. Exiting.")
        return

    print(f"Using {len(bus_schedule)} GTFS-based departure times.\n")

    # 2. Calculate lateness probability curve
    leave_times, P_of_being_late = calculate_late_probability(
        bus_times=bus_schedule,
        walk_to_bus=300,
        walk_to_work=240,
        meeting_time="09:05:00"
    )

    # 3. Save results
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "late_probabilities.csv")

    df = pd.DataFrame({
        "departure_time": leave_times,
        "late_probability": P_of_being_late
    })
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}.\n")

    # 4. Print short overview
    print("Bus schedule overview (first 5 entries):")
    for dep, arr in bus_schedule[:5]:
        print(f"Dep: {dep} → Arr: {arr}")
    if len(bus_schedule) > 5:
        print("...")

    # 5. Plot results
    plot_late_probabilities(
        leave_times,
        P_of_being_late,
        save_path=os.path.join(output_dir, "late_probability_plot.png")
    )

if __name__ == "__main__":
    main()
