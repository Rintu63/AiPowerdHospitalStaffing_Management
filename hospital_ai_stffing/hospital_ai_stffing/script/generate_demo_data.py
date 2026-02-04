import pandas as pd
import os
from datetime import datetime, timedelta
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
SNAPSHOT_PATH = os.path.join(DATA_DIR, "daily_snapshot.csv")

# ✅ CREATE data/ DIRECTORY IF NOT EXISTS
os.makedirs(DATA_DIR, exist_ok=True)

start_date = datetime.today() - timedelta(days=29)
dates = [start_date + timedelta(days=i) for i in range(30)]

rows = []

for d in dates:
    rows.append({
        "date": d.date().isoformat(),
        "doctors": random.randint(35, 45),
        "nurses": random.randint(80, 110),
        "sisters": random.randint(25, 35),
        "patients_opd": random.randint(250, 420),
        "patients_emergency": random.randint(90, 180),
        "patients_icu": random.randint(30, 60),
    })

df = pd.DataFrame(rows)

df.to_csv(SNAPSHOT_PATH, index=False)

print("✅ Demo data created at:", SNAPSHOT_PATH)
