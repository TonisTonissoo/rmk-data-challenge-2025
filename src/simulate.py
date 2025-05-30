import random
from datetime import datetime, timedelta


def generate_bus_schedule(start_time_str, end_time_str, interval_minutes=10, jitter_seconds=60):
    """
    Generates a list of simulated bus departure times with optional jitter.

    Args:
        start_time_str (str): Start of the time window in format 'HH:MM'
        end_time_str (str): End of the time window in format 'HH:MM'
        interval_minutes (int): Planned interval between buses
        jitter_seconds (int): Max random deviation (+/-) in seconds

    Returns:
        List[datetime]: List of bus departure times with jitter
    """
    time_format = "%H:%M"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    bus_times = []
    current = start_time

    while current <= end_time:
        jitter = timedelta(seconds=random.randint(-jitter_seconds, jitter_seconds))
        departure_time = current + jitter
        bus_times.append(departure_time)
        current += timedelta(minutes=interval_minutes)
    
    return sorted(bus_times)


def calculate_late_probability(
    departure_time_str,
    bus_schedule,
    walk_to_stop_sec=300,
    walk_from_stop_sec=240,
    ride_mean_min=20,
    ride_std_min=3,
    meeting_time_str="09:05",
    n_simulations=1000
):
    """
    Simulates the probability that Rita is late to her meeting
    given a home departure time.

    Args:
        departure_time_str (str): Time Rita leaves home (e.g. "08:10")
        bus_schedule (List[datetime]): Simulated list of bus departure times
        walk_to_stop_sec (int): Seconds from home to the stop
        walk_from_stop_sec (int): Seconds from stop to the office
        ride_mean_min (int): Average ride duration in minutes
        ride_std_min (int): Std deviation of ride time in minutes
        meeting_time_str (str): Meeting time (e.g. "09:05")
        n_simulations (int): Number of Monte Carlo simulations

    Returns:
        float: Probability (0–1) that Rita is late
    """
    time_format = "%H:%M"
    departure_time = datetime.strptime(departure_time_str, time_format)
    meeting_time = datetime.strptime(meeting_time_str, time_format)

    late_count = 0

    for _ in range(n_simulations):
        # Step 1: Walk from home to stop
        arrival_at_stop = departure_time + timedelta(seconds=walk_to_stop_sec)

        # Step 2: Find first bus that departs after arrival at stop
        next_bus = next((b for b in bus_schedule if b >= arrival_at_stop), None)

        if next_bus is None:
            late_count += 1  # No bus available
            continue

        # Step 3: Simulate ride duration
        ride_duration = max(0, random.gauss(ride_mean_min, ride_std_min))
        ride_time = timedelta(minutes=ride_duration)

        # Step 4: Walk from stop to meeting room
        total_arrival = next_bus + ride_time + timedelta(seconds=walk_from_stop_sec)

        if total_arrival > meeting_time:
            late_count += 1

    return late_count / n_simulations
