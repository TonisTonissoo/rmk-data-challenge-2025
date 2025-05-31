import requests
import pandas as pd
from io import StringIO
from datetime import datetime

def download_and_save_line8_realtime(save_path="data/raw/bus_line8_realtime.csv"):
    url = "https://transport.tallinn.ee/gps.txt"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch data.")
        return

    # Read text into DataFrame
    df = pd.read_csv(StringIO(response.text), sep="\t")

    # Filter for line 8 only
    df_line8 = df[df["line"] == 8]

    # Optional: parse time or convert fields
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_line8["fetched_at"] = now

    df_line8.to_csv(save_path, index=False)
    print(f"Saved {len(df_line8)} real-time records for line 8 to {save_path}")
