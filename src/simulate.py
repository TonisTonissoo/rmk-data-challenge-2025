from datetime import datetime, timedelta

def calculate_late_probability(
    bus_times: list,
    walk_to_bus: int = 300,
    walk_to_work: int = 240,
    meeting_time: str = '09:05:00',
    start_check: str = '07:00',
    end_check: str = '09:00'
) -> list:
    """
    Calculates probability of being late to a meeting depending on departure time.

    Args:
        bus_times (list): List of [departure_time (time), arrival_time (time)] pairs
        walk_to_bus (int): Time in seconds to reach bus stop
        walk_to_work (int): Time in seconds from bus stop to office
        meeting_time (str): Meeting start time (format "HH:MM:SS")
        start_check (str): Start of home departure range (format "HH:MM")
        end_check (str): End of home departure range (format "HH:MM")

    Returns:
        list: [x_axis_labels, probabilities]
    """
    walk_to_bus = timedelta(seconds=walk_to_bus)
    walk_to_work = timedelta(seconds=walk_to_work)
    meeting_dt = datetime.strptime(meeting_time, "%H:%M:%S")

    start_dt = datetime.strptime(start_check, "%H:%M")
    end_dt = datetime.strptime(end_check, "%H:%M")
    total_minutes = int((end_dt - start_dt).total_seconds() // 60)

    x_axis = []
    y_axis = []
    last_chance = None
    insert_index = None

    for minute in range(total_minutes + 1):
        leave_dt = start_dt + timedelta(minutes=minute)
        arrive_stop = leave_dt + walk_to_bus

        # Find next available bus
        bus_found = False
        for dep_time, arr_time in bus_times:
            dep_dt = datetime.combine(leave_dt.date(), dep_time)
            arr_dt = datetime.combine(leave_dt.date(), arr_time)
            if dep_dt >= arrive_stop:
                final_arrival = arr_dt + walk_to_work
                bus_found = True
                break

        probability = 1 if not bus_found or final_arrival > meeting_dt else 0

        x_label = leave_dt.strftime("%H:%M")
        x_axis.append(x_label)
        y_axis.append(probability)

        if probability == 0:
            last_chance = leave_dt
        elif len(y_axis) > 1 and y_axis[-2] == 0:
            insert_index = len(y_axis)

    # Insert threshold edge point
    if insert_index is not None and last_chance is not None:
        x_axis.insert(insert_index, (last_chance + timedelta(seconds=1)).strftime("%H:%M"))
        y_axis.insert(insert_index, 1)

    return [x_axis, y_axis]
