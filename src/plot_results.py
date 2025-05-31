import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_late_probabilities(csv_path, save_path=None):
    """
    Plots the probability of being late based on departure time.

    Args:
        csv_path (str): Path to the CSV file with 'departure_time' and 'late_probability'
        save_path (str, optional): If provided, saves the plot to this file path
    """
    # Load data
    df = pd.read_csv(csv_path)
    df["departure_time"] = pd.to_datetime(df["departure_time"], format="%H:%M")

    # Setup plot
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Plot
    ax.plot(df["departure_time"], df["late_probability"], marker='o', linestyle='-', color='tab:blue', label='Late Probability')

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))  # tick every 10 min
    plt.xticks(rotation=45)

    # Axis labels and title
    plt.xlabel("Time Leaving Home", fontsize=12)
    plt.ylabel("Probability of Being Late", fontsize=12)
    plt.title("Rita's Late Probability Based on Departure Time", fontsize=14)

    # Grid and style
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.ylim(-0.05, 1.05)
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")

    plt.show()
