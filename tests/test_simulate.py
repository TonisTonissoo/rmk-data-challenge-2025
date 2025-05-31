import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.simulate import generate_bus_schedule, calculate_late_probability


"""
Unit tests for simulation functions used to model lateness to a meeting based on public transportation.

This test module includes:
- Tests for correct generation of bus schedules with and without jitter.
- Tests for lateness probability calculation using different bus schedule scenarios:
  * A normal case where buses are frequent and lateness is rare.
  * An edge case where no buses are available, ensuring lateness is guaranteed.

Functions tested:
- generate_bus_schedule
- calculate_late_probability
"""

def test_generate_bus_schedule_length():
    buses = generate_bus_schedule("08:00", "08:30", interval_minutes=10, jitter_seconds=0)
    assert len(buses) == 4  # 08:00, 08:10, 08:20, 08:30

def test_generate_bus_schedule_order():
    buses = generate_bus_schedule("08:00", "08:30", interval_minutes=10, jitter_seconds=30)
    assert buses == sorted(buses)  # Times should be sorted

def test_calculate_late_probability_never_late():
    buses = generate_bus_schedule("08:00", "09:00", interval_minutes=5, jitter_seconds=0)
    prob = calculate_late_probability(
        departure_time_str="08:00",
        bus_schedule=buses,
        ride_mean_min=10,
        ride_std_min=1,
        walk_to_stop_sec=0,
        walk_from_stop_sec=0,
        meeting_time_str="09:05",
        n_simulations=100
    )
    assert 0.0 <= prob <= 0.05  # Should rarely be late

def test_calculate_late_probability_always_late():
    # Simulate unrealistic case: no buses available
    buses = []
    prob = calculate_late_probability(
        departure_time_str="08:55",
        bus_schedule=buses,
        ride_mean_min=10,
        ride_std_min=1,
        walk_to_stop_sec=0,
        walk_from_stop_sec=0,
        meeting_time_str="09:05",
        n_simulations=10
    )
    assert prob == 1.0
