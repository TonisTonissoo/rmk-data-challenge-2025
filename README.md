# RMK Data Challenge 2025 — Late Probability Simulation

This project simulates the probability of being late to a 9:05 AM meeting when commuting by bus (Line 8, Zoo → Toompark) using real GTFS data from [Peatus.ee](https://peatus.ee/).

---

## Features

- Downloads and parses real GTFS data
- Filters for Line 8 (Zoo → Toompark) weekday trips
- Simulates lateness probability based on home departure time
- Plots a clear time-vs-lateness probability graph
- Highlights the last safe departure time
- Includes unit tests for core simulation logic

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rmk-data-challenge-2025.git
cd rmk-data-challenge-2025
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the simulation

```bash
python main.py
```

This will:

- Download and extract GTFS data
- Parse valid Line 8 trips (Zoo → Toompark)
- Simulate lateness probabilities for each departure time
- Save the results to `data/processed/`
- Display and save a visual plot of probabilities

---

## Project Structure

```
.
├── main.py                     # Main script to run the pipeline
├── src/
│   ├── simulate.py             # Logic to calculate lateness probability
│   ├── load_gtfs_schedule.py  # Load and filter GTFS data for relevant trips
│   └── plot_results.py        # Generate and annotate the plot
├── tests/
│   └── test_simulate.py       # Unit tests for core logic
├── data/
│   └── processed/             # Output files (CSV + plot)
├── requirements.txt
└── README.md
```

---

## Output

- **CSV**: `data/processed/late_probabilities.csv` — departure times with corresponding lateness probabilities
- **Plot**: `data/processed/late_probability_plot.png` — includes:
  - Lateness probability curve
  - Red dot and label for last safe departure
  - Dashed vertical line marking the meeting time (09:05)
  - X-axis ticks every 15 minutes

---

## Configuration

Defaults in `main.py`:

- Meeting time: `09:05`
- Walk to bus stop: 300 seconds (5 minutes)
- Walk from bus to meeting: 240 seconds (4 minutes)

These can be customized by changing function arguments in the script.

---

## Testing

To run unit tests:

```bash
pytest tests/
```

---