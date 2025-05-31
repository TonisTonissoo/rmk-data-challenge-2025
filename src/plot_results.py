import pandas as pd
import matplotlib.pyplot as plt

def plot_late_probabilities(csv_path, save_path=None):
    """
    Plots the probability of being late based on departure time.

    Args:
        csv_path (str): Path to the CSV file with 'departure_time' and 'late_probability'
        save_path (str, optional): If provided, saves the plot to this file path
    """
    df = pd.read_csv(csv_path)
    df["departure_time"] = pd.to_datetime(df["departure_time"], format="%H:%M")

    plt.figure(figsize=(10, 5))
    plt.plot(df["departure_time"], df["late_probability"], marker='o', linestyle='-')
    plt.title("Probability of Being Late vs Departure Time")
    plt.xlabel("Departure Time from Home")
    plt.ylabel("Probability of Being Late")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")

    plt.show()