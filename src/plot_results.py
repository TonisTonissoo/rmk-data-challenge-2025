import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_late_probabilities(csv_path, save_path=None):
    """
    Plots the probability of being late based on departure time.
    """
    df = pd.read_csv(csv_path)

    # Convert time strings to datetime objects (arbitrary date)
    df["departure_time"] = pd.to_datetime(df["departure_time"], format="%H:%M")

    # Prepare figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot late probability curve
    ax.plot(df["departure_time"], df["late_probability"], marker='o', linestyle='-', color='steelblue', label="Late probability")

    # Find last safe time
    on_time_rows = df[df["late_probability"] == 0]
    last_safe_dt = on_time_rows["departure_time"].max() if not on_time_rows.empty else None

    # Annotate last safe departure
    if last_safe_dt:
        ax.plot(last_safe_dt, 0, marker='o', color='red', markersize=8)
        ax.annotate("Last safe\ndeparture", 
                    xy=(last_safe_dt, 0), 
                    xytext=(-40, 30),
                    textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', color='gray'),
                    fontsize=9,
                    ha='right')
    else:
        ax.text(0.5, 0.5, "No safe departure time!", transform=ax.transAxes,
                fontsize=14, color="red", ha='center')

    # Add vertical dashed line for meeting time at 09:05
    meeting_time = datetime.strptime("09:05", "%H:%M")
    ax.axvline(x=meeting_time, color='gray', linestyle='dashed', linewidth=1)
    ax.text(meeting_time, 1.02, 'Meeting time', color='gray', fontsize=9, rotation=90, ha='center')

    # Format x-axis ticks to show only HH:MM and space every 15 minutes
    start = df["departure_time"].min().replace(second=0)
    end = df["departure_time"].max().replace(second=0)
    tick_times = [start + timedelta(minutes=15*i) for i in range(int((end - start).seconds / 60 // 15) + 2)]

    ax.set_xticks(tick_times)
    ax.set_xticklabels([t.strftime("%H:%M") for t in tick_times], rotation=45)

    # Labels and layout
    ax.set_title("Rita's Late Probability Based on Departure Time")
    ax.set_xlabel("Time Leaving Home")
    ax.set_ylabel("Probability of Being Late")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")

    plt.show()
