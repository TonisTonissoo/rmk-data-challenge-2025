import pandas as pd
import matplotlib.pyplot as plt

def plot_late_probabilities(csv_path):
    """
    Plots the probability of being late to the meeting
    based on departure time from home.

    Args:
        csv_path (str): Path to the CSV file with 'departure_time' and 'late_probability' columns
    """
    df = pd.read_csv(csv_path)

    # Convert departure_time to datetime.time for proper plotting
    df["departure_time"] = pd.to_datetime(df["departure_time"], format="%H:%M")

    plt.figure(figsize=(10, 5))
    plt.plot(df["departure_time"], df["late_probability"], marker='o', linestyle='-')

    plt.title("Probability of Being Late vs Departure Time")
    plt.xlabel("Departure Time from Home")
    plt.ylabel("Probability of Being Late")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
