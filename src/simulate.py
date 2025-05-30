import random
from datetime import datetime, timedelta

def generate_bus_schedule(start_time_str, end_time_str, interval_minutes=10, jitter_seconds=60):
    """
    Generates a list of simulated bus arrival times with optional jitter.
    
    Args:
        start_time_str (str): Start of the time window in format 'HH:MM'
        end_time_str (str): End of the time window in format 'HH:MM'
        interval_minutes (int): Planned interval between buses
        jitter_seconds (int): Maximum random deviation (+/-) in seconds
    
    Returns:
        List[datetime]: List of bus arrival times with jitter
    """
    time_format = "%H:%M"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    bus_times = []
    current = start_time

    while current <= end_time:
        jitter = timedelta(seconds=random.randint(-jitter_seconds, jitter_seconds))
        arrival_time = current + jitter
        bus_times.append(arrival_time)
        current += timedelta(minutes=interval_minutes)
    
    return sorted(bus_times)
